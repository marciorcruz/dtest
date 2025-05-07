class Money:
    def __init__(self, amount: int):
        if amount < 0:
            raise ValueError("Money amount cannot be negative")
        self.amount = amount

    def __add__(self, other: "Money") -> "Money":
        return Money(self.amount + other.amount)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Money) and self.amount == other.amount