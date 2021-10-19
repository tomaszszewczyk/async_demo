def yield_fibonacci(i):
    a, b = 1, 1
    for _ in range(i):
        yield a
        b, a = a + b, b


if __name__ == "__main__":
    for f in yield_fibonacci(10):
        print(f)
