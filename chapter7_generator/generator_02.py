class NumberSequence:
    def __init__(self, start=0):
        self.current = start

    def next(self):
        current = self.current
        self.current += 1
        return current


if __name__ == "__main__":
    seq = NumberSequence(10)
    print(seq.next())
    print(seq.next())
    print(seq.next())