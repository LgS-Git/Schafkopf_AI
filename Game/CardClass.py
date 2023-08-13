class Card:
    SUITS = ['Schelle', 'Herz', 'Blatt', 'Eichel']
    RANKS = ["7", "8", "9", "König", "10", "Ass", "Unter", "Ober"]
    VALUES = [0, 0, 0, 4, 10, 11, 2, 3]

    def __init__(self, suit, rank):
        if suit not in Card.SUITS or rank not in Card.RANKS:
            raise ValueError("Invalid suit or rank")
        self.suit = suit
        self.rank = rank
        self.value = Card.VALUES[Card.RANKS.index(rank)]

    def __str__(self):
        return f"{self.suit}|{self.rank}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, Card):
            return self.suit == other.suit and self.rank == other.rank
        return False
