def failing_generator():
    yield 0
    raise Exception("Generator error")
    yield 1


def wrapper_generator():
    try:
        yield from failing_generator()
    except:
        print("Something went wrong")


if __name__ == "__main__":
    for f in wrapper_generator():
        print(f)
