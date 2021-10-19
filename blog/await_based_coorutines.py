counter = 0


class WaitB:
    def __await__(self):
        yield "B"


class WaitC:
    def __await__(self):
        yield "C"


async def coorutine():
    global counter
    id = counter
    counter += 1

    print(f"{id} Processing event A, blocking on B")
    await WaitB()
    print(f"{id} Processing event B, blocking on C")
    await WaitC()
    print(f"{id} Processing event C, task done")


def app():
    tasks = {"A": [], "B": [], "C": []}
    while True:
        print(f"Task queue size {len(tasks['A'] + tasks['B'] + tasks['C'])}")
        event = input("> ").strip()

        if event == "A":
            new_task = coorutine()
            waiting_for = new_task.send(None)
            tasks[waiting_for].append(new_task)

        if len(tasks[event]):
            task = tasks[event][0]
            tasks[event].remove(task)
            try:
                waiting_for = task.send(None)
                tasks[waiting_for].append(task)
            except StopIteration:
                pass


if __name__ == "__main__":
    app()
