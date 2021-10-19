class Task:
    COUNTER = 0

    def __init__(self):
        self.state = "AWAITING A"
        self.id = Task.COUNTER
        Task.COUNTER += 1

    def process_a(self):
        print(f"{self.id} Processing event A, blocking on B")
        self.state = "AWAITING B"
        return True

    def process_b(self):
        print(f"{self.id} Processing event B, blocking on C")
        self.state = "AWAITING C"
        return True

    def process_c(self):
        print(f"{self.id} Processing event C, task done")
        self.state = "DONE"
        return True

    def process_new_event(self, event):
        if self.state == "AWAITING A" and event == "A":
            return self.process_a()

        if self.state == "AWAITING B" and event == "B":
            return self.process_b()

        if self.state == "AWAITING C" and event == "C":
            return self.process_c()

        return False


def app():
    tasks = []
    while True:
        print(f"Task queue size {len(tasks)}")
        event = input("> ").strip()

        if event == "A":
            tasks.append(Task())

        for task in tasks:
            if task.process_new_event(event):
                if task.state == "DONE":
                    tasks.remove(task)
                break


if __name__ == "__main__":
    app()
