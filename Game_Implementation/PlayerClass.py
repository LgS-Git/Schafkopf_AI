import random


class Player:

    def __init__(self, name):
        self.name = name
        self.hand = []

    def receive_cards(self, cards):
        self.hand.extend(cards)

    def play_card(self):
        # AI plays card (for now random card from hand)
        card = random.choice(self.hand)
        return self.hand.pop(card)

    def klopfen(self):
        # Decide whether to klopfen (for now klopfen half the time)
        klopfen_choice = random.choice([True, False])
        return klopfen_choice

    def contra(self):
        # Decide whether to contra (for now contra half the time)
        contra_choice = random.choice([True, False])
        return contra_choice

    def re(self):
        # Decide whether to contra (for now re half the time)
        re_choice = random.choice([True, False])
        return re_choice

    def decide_game_type(self, position):
        if position < 4:
            game_type_choice = random.choice([random.choice(['Rufspiel-Eichel', 'Rufspiel-Blatt', 'Rufspiel-Herz', 'Rufspiel-Schelle',
                                                             'Solo-Eichel', 'Solo-Blatt', 'Solo-Herz', 'Solo-Schelle', 'Wenz']), 'Passen'])
        else:
            game_type_choice = random.choice(['Rufspiel-Eichel', 'Rufspiel-Blatt', 'Rufspiel-Herz', 'Rufspiel-Schelle',
                                              'Solo-Eichel', 'Solo-Blatt', 'Solo-Herz', 'Solo-Schelle', 'Wenz'])
        return game_type_choice

    def __str__(self):
        return f"{self.name} has {len(self.hand)} cards"

    def __eq__(self, other):
        if isinstance(other, Player):
            return self.name == other.name
        return False
