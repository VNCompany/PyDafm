class Priority:
    id = -1
    name = ""
    color = ""

    def __init__(self, ident, name, color):
        self.id = int(ident)
        self.name = str(name)
        self.color = color

    def __str__(self):
        return str(self.id)


class Debtor:
    id = -1
    name = ""
    priority = 0

    def __init__(self, ident, name, priority):
        self.id = ident
        self.name = name
        self.priority = priority

    def __str__(self):
        return str(self.name)


class Debt:
    id = -1
    debtor = ""
    amount = 0
    description = ""
    priority = 0
    date = ""

    def __init__(self, ident, debtor, amount, desc, priority, date):
        self.id = ident
        self.debtor = debtor
        self.amount = amount
        self.description = desc
        self.priority = priority
        self.date = date

    def __str__(self):
        return self.description
