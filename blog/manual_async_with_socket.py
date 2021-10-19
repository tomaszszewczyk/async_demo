import socket
import selectors


class AsyncServer:
    SERVER_ADDRESS = ("localhost", 6666)

    def __init__(self, selector: selectors.BaseSelector):
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_server.setblocking(False)
        self.socket_server.bind(self.SERVER_ADDRESS)
        self.socket_server.listen()
        selector.register(self.socket_server.fileno(), selectors.EVENT_WRITE | selectors.EVENT_READ)

    def get_fd(self) -> int:
        return self.socket_server.fileno()

    def accept(self) -> socket.socket:
        (client_socket, address) = self.socket_server.accept()
        return client_socket

    def close(self):
        self.socket_server.close()


class AsyncClient:
    TARGET_ADDRESS = ("localhost", 8080)

    def __init__(self, selector: selectors.BaseSelector):
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_client.setblocking(False)
        try:
            selector.register(self.socket_client.fileno(), selectors.EVENT_WRITE | selectors.EVENT_READ)
        except KeyError:
            pass

    def get_fd(self):
        return self.socket_client.fileno()

    def connect(self):
        self.socket_client.connect(self.TARGET_ADDRESS)

    def send_request(self):
        self.socket_client.send("GET /rate HTTP/1.1\n\n".encode())

    def read_response(self):
        return self.socket_client.recv(1000).decode()

    def close(self):
        self.socket_client.close()


class Request:
    def __init__(self, request_socket: socket.socket, selector: selectors.BaseSelector):
        self.request_socket = request_socket
        self.selector = selector
        self.rate_client = AsyncClient(self.selector)
        self.state = "READING_REQUEST"

    def get_fd(self):
        if self.state == "READING_REQUEST" or self.state == "RESPONDING":
            return self.request_socket.fileno()
        elif self.state == "CONNECTING" or self.state == "WRITING" or self.state == "READING":
            return self.rate_client.get_fd()

    def set_state(self, state):
        old_state = self.state
        self.state = state
        print(f'{old_state} -> {state}')

    @staticmethod
    def extract_rate(response):
        return int(response.split('\n')[-1])

    def process(self):
        try:
            if self.state == "READING_REQUEST":
                rx_data = self.request_socket.recv(1000).decode()
                print(rx_data)
                if rx_data.startswith("GET"):
                    self.set_state("CONNECTING")
                    self.rate_client.connect()
                    self.process()

            elif self.state == "CONNECTING":
                self.set_state("WRITING")
                self.rate_client.send_request()
                self.process()

            elif self.state == "WRITING" or self.state == "READING":
                self.set_state("READING")
                self.rate = self.extract_rate(self.rate_client.read_response())
                self.rate_client.close()
                self.set_state("RESPONDING")
                self.request_socket.send(str(self.rate * 10).encode())
                self.process()

            elif self.state == "RESPONDING":
                self.set_state("DONE")
                self.request_socket.close()

        except BlockingIOError:
            print("blocking on state", self.state)


class AsyncApp:
    def __init__(self):
        self.selector = selectors.DefaultSelector()
        self.server = AsyncServer(self.selector)
        self.pending_requests = []

    def run(self):
        try:
            self.mainloop()
        finally:
            self.server.close()

    def mainloop(self):
        while True:
            events = self.selector.select()
            for selector_key, event in events:
                if selector_key.fd == self.server.get_fd():
                    self.create_new_request()

                for request in self.pending_requests:
                    if selector_key.fd == request.get_fd():
                        request.process()

    def create_new_request(self):
        request = Request(self.server.accept(), self.selector)
        self.pending_requests.append(request)
        request.process()


if __name__ == "__main__":
    app = AsyncApp()
    app.run()
