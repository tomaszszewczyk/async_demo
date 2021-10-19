def step_generator(start, stop, step):
    i = 0
    while start + step * i != stop:
        yield start + step * i
        i += 1


def wrapper_generator(start, stop):
    yield from step_generator(start, stop, 1)
    yield from step_generator(stop, start, -1)


if __name__ == "__main__":
    for f in wrapper_generator(0, 5):
        print(f)
