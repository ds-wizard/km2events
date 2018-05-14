import uuid


class UUIDGenerator:

    def __init__(self):
        self.used = set()  # type: Set[str]

    def __next__(self):
        while True:
            yield self.generate()

    def generate(self):
        result = str(uuid.uuid4())
        while result in self.used:
            print(result)
            result = str(uuid.uuid4())
        self.use(result)
        return result

    def use(self, *args):
        self.used.union(set(args))
