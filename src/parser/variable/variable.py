class Variable:
    name: str

    def __init__(self, name_: str):
        self.name = name_

    def print(self):
        print('Name: ' + self.name)


