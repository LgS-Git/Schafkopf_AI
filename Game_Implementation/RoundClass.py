from DeckClass import Deck
from CardClass import Card


class Round:

    def __init__(self, players, start_player_index):
        self.players = players

        self.deck = Deck()
        self.game_type = None  # Rufspiel-Eichel, Rufspiel-Blatt, Rufspiel-Herz, Rufspiel-Schelle, Solo-Eichel, Solo-Blatt, Solo-Herz, Solo-Schelle, Wenz
        self.trumps_in_order = []
        self.klopfen_players = []
        self.kontra_players = []
        self.re_players = []
        self.round_scores = {player.name: 0 for player in players}
        self.tricks_per_player = {player.name: [] for player in players}
        self.current_trick = []
        self.current_trick_number = 0
        self.current_player_index = start_player_index  # 0 --> Player 1, 1 --> Player 2, 2 --> Player 3 etc.
        self.play_caller = None

    def set_klopfen(self, player):
        if player.klopfen():
            self.klopfen_players.append(player)

    def set_kontra(self, player):
        if player.kontra():
            self.kontra_players.append(player)

    def set_re(self, player):
        if player.re():
            self.re_players.append(player)

    def set_game_type(self, player, game_type):
        self.game_type = (player.name, game_type)

        if self.game_type[1] in ['Rufspiel-Eichel', 'Rufspiel-Blatt', 'Rufspiel-Herz', 'Rufspiel-Schelle']:
            self.trumps_in_order = [Card(suit, 'Unter') for suit in Card.SUITS] + \
                [Card(suit, 'Ober') for suit in Card.SUITS]
        elif self.game_type[1] in ['Solo-Eichel', 'Solo-Blatt', 'Solo-Herz', 'Solo-Schelle']:
            solo_suit = self.game_type[1].split('-')[1]
            self.trumps_in_order = [Card(solo_suit, rank) for rank in Card.RANKS if rank not in ['Ober', 'Unter']] + \
                [Card(suit, 'Unter') for suit in Card.SUITS] + \
                [Card(suit, 'Ober') for suit in Card.SUITS]
        elif self.game_type[1] == 'Wenz':
            self.trumps_in_order = [Card(suit, 'Unter') for suit in Card.SUITS]

    def deal(self):
        self.deck.shuffle()
        for player in self.players:
            player.receive_cards(self.deck.deal())

    def determine_trick_winner(self):
        if len(self.current_trick) < 4:
            print('Trick not finished, continue playing')
            return

        leading_suit = self.current_trick[0][1].suit
        highest_card = self.current_trick[0][1]
        winning_player = self.current_trick[0][0]
        trick_won = (self.current_trick[0][1], None, None, None)

        index = 0
        for player, card in self.current_trick[1:]:
            is_card_trump = card in self.trumps_in_order
            is_highest_card_trump = highest_card in self.trumps_in_order
            is_same_suit_as_leading = card.suit == leading_suit

            if is_card_trump and is_highest_card_trump:
                if self.trumps_in_order.index(card) > self.trumps_in_order.index(highest_card):
                    highest_card = card
                    winning_player = player
            elif is_card_trump and not is_highest_card_trump:
                highest_card = card
                winning_player = player
            elif is_same_suit_as_leading and not is_highest_card_trump:
                if (Card.RANKS.index(card.rank) > Card.RANKS.index(highest_card.rank)):
                    highest_card = card
                    winning_player = player

            trick_won[index + 1] = card
            index += 1

        return winning_player, trick_won

    def play_trick(self):

        self.current_trick_number += 1

        for _ in range(4):
            player = self.players[self.current_player_index]
            card = player.play_card()  # Player decides which card to play
            self.current_trick.append((player, card))
            self.current_player_index = (self.current_player_index + 1) % 4

        winning_player, trick_won = self.determine_trick_winner()

        self.tricks_per_player[winning_player.name].append(trick_won)

        # Reset the current trick
        self.current_trick = []

        self.current_player_index = self.players.index(winning_player)

    def play_round(self):

        # In order to start pre-round loops with start_player
        players_in_order = self.players[self.start_player_index:] + self.players[:self.start_player_index]

        # Pre-round decisions
        for player in players_in_order:
            self.set_klopfen(player)

        for player in players_in_order:
            game_type = player.decide_game_type()
            if game_type is not 'Passen':
                self.set_game_type(player, game_type)
                self.play_caller = player
                break

        match game_type:
            case 'Rufspiel-Eichel':
                for player in players_in_order:
                    if player != self.play_caller and Card('Eichel', 'Ass') not in player.hand:
                        self.set_kontra(player)

                if self.kontra_players:
                    for player in players_in_order:
                        if player != self.play_caller and Card('Eichel', 'Ass') not in player.hand:
                            continue
                        self.set_re(player)

            case 'Rufspiel-Blatt':
                for player in players_in_order:
                    if player != self.play_caller and Card('Blatt', 'Ass') not in player.hand:
                        self.set_kontra(player)

                if self.kontra_players:
                    for player in players_in_order:
                        if player != self.play_caller and Card('Blatt', 'Ass') not in player.hand:
                            continue
                        self.set_re(player)

            case 'Rufspiel-Herz':
                for player in players_in_order:
                    if player != self.play_caller and Card('Herz', 'Ass') not in player.hand:
                        self.set_kontra(player)

                if self.kontra_players:
                    for player in players_in_order:
                        if player != self.play_caller and Card('Herz', 'Ass') not in player.hand:
                            continue
                        self.set_re(player)

            case 'Rufspiel-Schelle':
                for player in players_in_order:
                    if player != self.play_caller and Card('Schelle', 'Ass') not in player.hand:
                        self.set_kontra(player)

                if self.kontra_players:
                    for player in players_in_order:
                        if player != self.play_caller and Card('Schelle', 'Ass') not in player.hand:
                            continue
                        self.set_re(player)

            case 'Solo-Eichel' | 'Solo-Blatt' | 'Solo-Herz' | 'Solo-Schelle' | 'Wenz':
                for player in players_in_order:
                    if player != self.play_caller:
                        self.set_kontra(player)

                if self.kontra_players:
                    self.set_re(self.play_caller)

        # Play tricks
        while self.current_trick_number < 8:
            self.play_trick()

        # Calculate round points
        for player, tricks in self.tricks_per_player.items():
            total_points = 0
            for quadruple in tricks:
                for card in quadruple:
                    total_points += card.value
            self.round_scores[player] = total_points
