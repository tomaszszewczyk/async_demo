def step_generator(start, stop, step):
    i = 0
    while start + step * i != stop:
        yield start + step * i
        i += 1
    return i


def wrapper_generator():
    count = yield from step_generator(0, 10, 2)
    print(f"Generated {count} numbers")


if __name__ == "__main__":
    for f in wrapper_generator():
        print(f)
