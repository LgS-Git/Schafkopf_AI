import random
from .CardClass import Card


class Player:

    def __init__(self, name):
        self.name = name
        self.hand = []

    def receive_cards(self, cards):
        self.hand.extend(cards)

    def play_card(self, game_type, current_trick):
        if len(self.hand) == 1:
            card = self.hand[0]
        if game_type in ['Rufspiel-Eichel', 'Rufspiel-Blatt', 'Rufspiel-Herz', 'Rufspiel-Schelle']:
            suit = game_type.split('-')[1]
            if len(current_trick) > 0 and current_trick[0][1].suit == suit and Card(suit, 'Ass') in self.hand:
                card = Card(suit, 'Ass')
            else:
                # AI plays card (for now random card from hand)
                card = random.choice(self.hand)
        else:
            # AI plays card (for now random card from hand)
            card = random.choice(self.hand)
        self.hand.remove(card)
        return card

    def klopfen(self):
        # Decide whether to klopfen (for now klopfen half the time)
        klopfen_choice = random.choice([True, False])
        return klopfen_choice

    def kontra(self):
        # Decide whether to contra (for now contra half the time)
        kontra_choice = random.choice([True, False])
        return kontra_choice

    def re(self):
        # Decide whether to contra (for now re half the time)
        re_choice = random.choice([True, False])
        return re_choice

    def tout(self):
        # Decide Tout on solo
        tout_choice = random.choice([True, False, False, False, False, False])
        return tout_choice

    def decide_game_type(self, position):
        # Possible game types per Hand
        possible_game_types = ['Rufspiel-Eichel', 'Rufspiel-Blatt', 'Rufspiel-Herz', 'Rufspiel-Schelle',
                               'Solo-Eichel', 'Solo-Blatt', 'Solo-Herz', 'Solo-Schelle', 'Wenz']
        for suit in Card.SUITS:
            if Card(suit, 'Ass') in self.hand:
                possible_game_types.remove(f'Rufspiel-{suit}')
            else:
                noTrump_ranks = [rank for rank in Card.RANKS if rank not in ['Ober', 'Unter']]
                if all(Card(suit, rank) not in self.hand for rank in noTrump_ranks):
                    possible_game_types.remove(f'Rufspiel-{suit}')

        # Decide what game to play
        if position < 4:
            game_type_choice = random.choice([random.choice(possible_game_types), 'Passen'])
        else:
            game_type_choice = random.choice(possible_game_types)
        return game_type_choice

    def __str__(self):
        return f"{self.name} ({len(self.hand)})"

    def __eq__(self, other):
        if isinstance(other, Player):
            return self.name == other.name
        return False
