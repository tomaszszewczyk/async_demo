def process_a():
    print("Processing event A")


def process_b():
    print("Processing event B")


def process_c():
    print("Processing event C")


def app():
    while True:
        event = input("> ").strip()

        if event == "A":
            process_a()
        elif event == "B":
            process_b()
        elif event == "C":
            process_c()


if __name__ == "__main__":
    app()
