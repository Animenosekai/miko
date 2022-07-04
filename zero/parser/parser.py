class Parser:
    def __init__(self, body: str) -> None:
        self.original = str(body)
        print("")
        print("")
        print(self.__class__.__name__)
        print("")
        print(self.original)
