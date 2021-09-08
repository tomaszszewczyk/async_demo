import select
import sys

poller = select.poll()
poller.register(sys.stdin.fileno(), select.POLLIN)

def application_logic():
    print("user input", input())

while False:
    events = poller.poll(1000)

    if len(events) == 0:
        print("timeout")

    for fd, event in events:
        if fd == sys.stdin.fileno() and event == select.POLLIN:
            application_logic()

class AsyncIO:
    def __init__(self, char):
        self.char = char

    def __await__(self):
        yield self


async def get_key(x):
    await AsyncIO(x)

async def async_app():
    x = 1
    print("first hello 111", x)
    await get_key('a')
    print("first hello 111", x)
    await get_key('b')

async def second_async_app():
    print("first hello 222")
    await get_key('c')
    print("first hello 222")
    await get_key('d')

def run(coroutines):
    waitings = {}

    for coor in coroutines:
        event = coor.send(None)
        waitings[event.char] = coor

    print(waitings)

    while waitings:
        events = poller.poll(1000)

        if len(events) == 0:
            print("timeout")

        for fd, event in events:
            if fd == sys.stdin.fileno() and event == select.POLLIN:
                chars = input()

                for char in chars:
                    try:
                        to_be_resumed = waitings.pop(char)
                    except KeyError:
                        continue

                    try:
                        new_event = to_be_resumed.send(char)
                    except StopIteration:
                        continue

                    if isinstance(new_event, AsyncIO):
                        waitings[new_event.char] = to_be_resumed

run([async_app(), second_async_app()])
