class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})
        return True

    def withdraw(self, amount, description=""):
        if amount > self.get_balance():
            return False
        self.ledger.append({"amount": -amount, "description": description})
        return True

    def get_balance(self):
        return sum(item["amount"] for item in self.ledger)

    def transfer(self, amount, category):
        if amount > self.get_balance():
            return False
        self.ledger.append({"amount": -amount, "description": "Transfer to " + category.name})
        category.ledger.append({"amount": amount, "description": "Transfer from " + self.name})
        return True

    def check_funds(self, amount):
        return amount <= self.get_balance()

    def __str__(self):
        total = self.get_balance()
        header = self.name.center(30, "*")
        lines = [header]
        for item in self.ledger:
            desc = item["description"][:23]
            lines.append("%-24s%6.2f" % (desc, item["amount"]))
        lines.append("Total: %.2f" % total)
        return "\n".join(lines)


def create_spend_chart(categories):
    spending = {}
    for cat in categories:
        s = 0
        for item in cat.ledger:
            if item["amount"] < 0:
                s += -item["amount"]
        spending[cat.name] = s
    total = sum(spending[cat.name] for cat in categories)
    if total == 0:
        return ""
    pcts = [spending[cat.name] / total * 100 for cat in categories]
    lines = ["Percentage spent by category"]
    for i in range(100, -1, -10):
        label = "%3d|" % i
        cells = ""
        for p in pcts:
            height = int(p) // 10 * 10
            cells += ("o" if height >= i else " ") + "  "
        lines.append(label + " " + cells)
    lines.append("    " + "-" * (3 * len(categories) + 1))
    names = [cat.name for cat in categories]
    maxlen = max((len(n) for n in names), default=0)
    for r in range(maxlen):
        row = ""
        for n in names:
            row += (n[r] if r < len(n) else " ") + "  "
        lines.append("     " + row)
    return "\n".join(lines)
