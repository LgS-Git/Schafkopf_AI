import numpy as np
from .CardClass import Card


class Deck:

    def __init__(self):
        self.cards = [Card(suit, rank) for suit in Card.SUITS for rank in Card.RANKS]

    def shuffle(self):
        np.random.shuffle(self.cards)

    def deal4(self):
        dealt_cards = self.cards[:4]
        self.cards = self.cards[4:]
        return dealt_cards

    def __str__(self):
        return f"Deck holds {len(self.cards)} Cards"
