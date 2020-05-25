from src.parser.variable.variable import Variable


class VariableTable:
    table: list

    def __init__(self):
        self.table = list()

    # Функция для добавления переменной в таблицу
    # Если переменная с таким именем уже существует то
    # возбуждается исключение
    # name - имя переменной
    def add(self, name: str):
        if self.contains(name):
            raise Exception("The variable '" + name + "' has already been declared!")

        self.table.append(Variable(name))

    # Функция проверяет наличие переменной с таким именем
    # name - имя переменной
    def contains(self, name: str) -> bool:
        for variable in self.table:
            if variable.name == name:
                return True
        return False

    # Функция для получения переменной по имени
    # В случае, если переменная не найдена возбуждается исключение
    # name - имя переменной
    def get(self, name: str) -> Variable:
        for variable in self.table:
            if variable.name == name:
                return variable
        raise Exception("Variable not found!")

    # Функция для печати таблицы
    def print(self):
        for variable in self.table:
            variable.print()

    def log_out(self):
        file = open("vars", "w")
        for variable in self.table:
            file.write("Name: " + variable.name)
            file.write("\n")
        file.close()