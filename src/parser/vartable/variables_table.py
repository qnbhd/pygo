class VariableTable:

    def __init__(self):
        self.table_ = dict()

    def put_variable(self, variable, value):
        if variable in self.table_:
            self.table_[variable].append(value)
        else:
            self.table_[variable] = [value]

    def var_is_exists(self, variable):
        if variable not in self.table_:
            return False
        return True

    def remove_variable(self, variable):
        if not self.var_is_exists(variable):
            raise Exception("Variable doesn't exist")
        self.table_[variable].pop()

    def get_variable(self, variable):
        if variable not in self.table_:
            return None
        return self.table_[variable][-1]


