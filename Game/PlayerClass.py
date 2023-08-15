from .CardClass import Card
import NEAT.network as AI
from NEAT.one_hot_functions import encode_game_state


class Player:

    def __init__(self, name, network):
        self.name = name
        self.hand = []  # List of card objects, if Card is played, it is replaced by None
        self.net = network

    def receive_cards(self, cards):
        self.hand.extend(cards)

    def count_cards_in_hand(self):
        return sum(1 for card in self.hand if card != None)

    def play_card(self, current_trick, tricks_per_player, players, starting_player, round_scores,
                  game_scores, kontra_player, re_player, tout_player, klopfen_players, game_type, trumps_in_order):
        # No decision if only one card
        if self.count_cards_in_hand() == 1:
            for card in self.hand:
                if card:
                    # Clear hand of None-Objects since last card
                    self.hand.clear()
                    return card

        # Determining suit or trump restriction if not first
        leading_suit = None
        leading_trump = False
        if len(current_trick) > 0:
            # Determine the leading card suit or trump
            leading_card = current_trick[0][1]
            if leading_card not in trumps_in_order:
                leading_suit = leading_card.suit
            else:
                leading_trump = True

            # Check if leading_suit or trump in Hand
            has_matching_suit = False
            has_trump = False
            for card in self.hand:
                if card:
                    if card.suit == leading_suit and card not in trumps_in_order:
                        has_matching_suit = True
                    if card in trumps_in_order:
                        has_trump = True

        # No decision if Ruf-Ass
        if game_type in ['Rufspiel-Eichel', 'Rufspiel-Blatt', 'Rufspiel-Herz', 'Rufspiel-Schelle']:
            suit = game_type.split('-')[1]
            if leading_suit == suit and Card(suit, 'Ass') in self.hand:
                card = Card(suit, 'Ass')

        # Create a mask for valid cards (there area also None-objects in hand which can't be played)
        valid_cards_mask = [1, 1, 1, 1, 1, 1, 1, 1]
        for idx, card in enumerate(self.hand):
            if not card:
                valid_cards_mask[idx] = -1
            elif leading_suit:
                if has_matching_suit and (card.suit != leading_suit or card in trumps_in_order):
                    valid_cards_mask[idx] = -1
            elif leading_trump:
                if has_trump and card not in trumps_in_order:
                    valid_cards_mask[idx] = -1

        # Network decides on card
        game_state = encode_game_state(self, current_trick, tricks_per_player, players, starting_player, round_scores,
                                       game_scores, kontra_player, re_player, tout_player, klopfen_players, game_type)
        network_output = self.net.activate(game_state)
        card = AI.decide_card_to_play(network_output, self, valid_cards_mask)

        # Replace card in hand with None
        idx = self.hand.index(card)
        self.hand[idx] = None
        return card

    def klopfen(self, current_trick, tricks_per_player, players, starting_player, round_scores,
                game_scores, kontra_player, re_player, tout_player, klopfen_players, game_type):
        game_state = encode_game_state(self, current_trick, tricks_per_player, players, starting_player, round_scores,
                                       game_scores, kontra_player, re_player, tout_player, klopfen_players, game_type)
        network_output = self.net.activate(game_state)
        return AI.decide_klopfen(network_output)

    def kontra(self, current_trick, tricks_per_player, players, starting_player, round_scores,
               game_scores, kontra_player, re_player, tout_player, klopfen_players, game_type):
        game_state = encode_game_state(self, current_trick, tricks_per_player, players, starting_player, round_scores,
                                       game_scores, kontra_player, re_player, tout_player, klopfen_players, game_type)
        network_output = self.net.activate(game_state)
        return AI.decide_kontra(network_output)

    def re(self, current_trick, tricks_per_player, players, starting_player, round_scores,
           game_scores, kontra_player, re_player, tout_player, klopfen_players, game_type):
        game_state = encode_game_state(self, current_trick, tricks_per_player, players, starting_player, round_scores,
                                       game_scores, kontra_player, re_player, tout_player, klopfen_players, game_type)
        network_output = self.net.activate(game_state)
        return AI.decide_re(network_output)

    def tout(self, current_trick, tricks_per_player, players, starting_player, round_scores,
             game_scores, kontra_player, re_player, tout_player, klopfen_players, game_type):
        game_state = encode_game_state(self, current_trick, tricks_per_player, players, starting_player, round_scores,
                                       game_scores, kontra_player, re_player, tout_player, klopfen_players, game_type)
        network_output = self.net.activate(game_state)
        return AI.decide_tout(network_output)

    def decide_game_type(self, current_trick, tricks_per_player, players, starting_player, round_scores,
                         game_scores, kontra_player, re_player, tout_player, klopfen_players, game_type, position):
        # Remove impossible game_types based on hand and position
        possible_game_types = ['Rufspiel-Eichel', 'Rufspiel-Blatt', 'Rufspiel-Herz', 'Rufspiel-Schelle',
                               'Solo-Eichel', 'Solo-Blatt', 'Solo-Herz', 'Solo-Schelle', 'Wenz', 'Passen']

        for suit in Card.SUITS:
            if Card(suit, 'Ass') in self.hand:
                possible_game_types.remove(f'Rufspiel-{suit}')
            else:
                noTrump_ranks = [rank for rank in Card.RANKS if rank not in ['Ober', 'Unter']]
                if all(Card(suit, rank) not in self.hand for rank in noTrump_ranks):
                    possible_game_types.remove(f'Rufspiel-{suit}')

        if position == 4:
            possible_game_types.remove('Passen')

        # Create network output
        game_state = encode_game_state(self, current_trick, tricks_per_player, players, starting_player, round_scores,
                                       game_scores, kontra_player, re_player, tout_player, klopfen_players, game_type)
        network_output = self.net.activate(game_state)

        return AI.decide_game_type(network_output, possible_game_types)

    def __str__(self):
        return f"{self.name} ({self.count_cards_in_hand})"

    def __eq__(self, other):
        if isinstance(other, Player):
            return self.name == other.name
        return False
