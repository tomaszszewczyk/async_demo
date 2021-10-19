def print_fibonacci(i):
    a, b = 1, 1
    for _ in range(i):
        print(a)
        b, a = a + b, b


if __name__ == "__main__":
    print_fibonacci(5)
