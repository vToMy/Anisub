class Name:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    @property
    def eastern_order(self):
        return f'{self.last_name} {self.first_name}'

    @property
    def western_order(self):
        return f'{self.first_name} {self.last_name}'
