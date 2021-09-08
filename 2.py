for x in [1, 2, 3]:
    print("array", x)

class AlleRange:
    def __init__(self, start, stop):
        self.start = start
        self.stop = stop

    def __iter__(self):
        self.counter = self.start
        return self

    def __next__(self):
        x = self.counter
        self.counter += 1

        if x == self.stop:
            raise StopIteration

        return x

for x in AlleRange(1, 4):
    print("iterator", x)

def alle_generator(start, stop):
    counter = start

    while counter < stop:
        yield counter
        counter += 1

for x in alle_generator(1, 4):
    print("generator", x)

def wrapped_generator():
    yield from alle_generator(1, 4)
    yield 10

for x in wrapped_generator():
    print("wrapped", x)

it = wrapped_generator()
print('next', next(it))
print('next', next(it))
print('next', next(it))

def super_alle_generator(start, stop):
    counter = start

    while counter < stop:
        x = yield counter
        counter += x

it = super_alle_generator(1, 100)
print("send", next(it))
print("send", it.send(10))
print("send", it.send(10))
print("send", it.send(10))
print("send", it.send(100))
