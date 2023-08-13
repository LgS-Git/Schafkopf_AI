from .DeckClass import Deck
from .CardClass import Card


class Round:

    def __init__(self, players, start_player_index, cumulative_score):
        self.players = players

        self.deck = Deck()
        self.game_type = ''  # Rufspiel-Eichel, Rufspiel-Blatt, Rufspiel-Herz, Rufspiel-Schelle, Solo-Eichel, Solo-Blatt, Solo-Herz, Solo-Schelle, Wenz
        self.trumps_in_order = []
        self.klopfen_players = []
        self.kontra_player = None
        self.re_player = None
        self.tout_player = None
        self.laufende = 0
        self.round_scores = {player.name: 0 for player in players}
        self.nonPlaying_team_score = 0
        self.playing_team_score = 0
        self.tricks_per_player = {player.name: [] for player in players}
        self.current_trick = []
        self.current_trick_number = 0
        self.current_player_index = start_player_index  # 0 --> Player 1, 1 --> Player 2, 2 --> Player 3 etc.
        self.starting_player = players[start_player_index] # Always holds who plays/played the first card in a trick
        self.play_caller = None
        self.playing_players = []
        self.nonPlaying_players = []
        self.starting_hand = {player.name: [] for player in players}
        self.current_game_score = cumulative_score

    def set_klopfen(self, player):
        if player.klopfen():
            self.klopfen_players.append(player)

    def set_kontra(self, player):
        if player.kontra():
            self.kontra_player = player

    def set_re(self, player):
        if player.re():
            self.re_player = player

    def set_tout(self, player):
        if player.tout():
            self.tout_player = player

    def set_trumps(self, game_type):

        if game_type in ['Rufspiel-Eichel', 'Rufspiel-Blatt', 'Rufspiel-Herz', 'Rufspiel-Schelle']:
            self.trumps_in_order = [Card(suit, 'Unter') for suit in Card.SUITS] + \
                [Card(suit, 'Ober') for suit in Card.SUITS]
        elif game_type in ['Solo-Eichel', 'Solo-Blatt', 'Solo-Herz', 'Solo-Schelle']:
            solo_suit = game_type.split('-')[1]
            self.trumps_in_order = [Card(solo_suit, rank) for rank in Card.RANKS if rank not in ['Ober', 'Unter']] + \
                [Card(suit, 'Unter') for suit in Card.SUITS] + \
                [Card(suit, 'Ober') for suit in Card.SUITS]
        elif game_type == 'Wenz':
            self.trumps_in_order = [Card(suit, 'Unter') for suit in Card.SUITS]

    def determine_trick_winner(self):
        if len(self.current_trick) < 4:
            print('Trick not finished, continue playing')
            return

        leading_suit = self.current_trick[0][1].suit
        highest_card = self.current_trick[0][1]
        winning_player = self.current_trick[0][0]

        for playerName, card in self.current_trick[1:]:
            is_card_trump = card in self.trumps_in_order
            is_highest_card_trump = highest_card in self.trumps_in_order
            is_same_suit_as_leading = card.suit == leading_suit

            if is_card_trump and is_highest_card_trump:
                if self.trumps_in_order.index(card) > self.trumps_in_order.index(highest_card):
                    highest_card = card
                    winning_player = playerName
            elif is_card_trump and not is_highest_card_trump:
                highest_card = card
                winning_player = playerName
            elif is_same_suit_as_leading and not is_highest_card_trump:
                if (Card.RANKS.index(card.rank) > Card.RANKS.index(highest_card.rank)):
                    highest_card = card
                    winning_player = playerName

        return winning_player

    def play_trick(self):

        self.current_trick_number += 1

        for _ in range(4):
            player = self.players[self.current_player_index]
            card = player.play_card(self.game_type, self.current_trick)  # Player decides which card to play
            self.current_trick.append((player.name, card))
            self.current_player_index = (self.current_player_index + 1) % 4

        winning_player = self.determine_trick_winner()

        only_cards_of_current_trick = tuple([tuple[1] for tuple in self.current_trick])
        self.tricks_per_player[winning_player].append(only_cards_of_current_trick)

        # Update round_scores
        trick_value = 0
        for _, card in self.current_trick:
            trick_value += card.value
        self.round_scores[winning_player] += trick_value

        # Reset the current trick and player index
        self.current_trick = []

        self.current_player_index = int(winning_player[-1]) - 1
        self.starting_player = self.players[self.current_player_index]

    def play_round(self):

        # In order to start pre-round loops with start_player
        players_in_order = self.players[self.current_player_index:] + self.players[:self.current_player_index]

        # Shuffle deck
        self.deck.shuffle()

        # Klopfen and Deal
        for player in players_in_order:
            player.receive_cards(self.deck.deal4())
            self.set_klopfen(player)
            player.receive_cards(self.deck.deal4())

        # Save starting hand
        for player in self.players:
            self.starting_hand[player.name] = player.hand.copy()

        # Game type decision
        position = 1
        for player in players_in_order:
            game_type = player.decide_game_type(position)
            position += 1
            if game_type != 'Passen':
                self.game_type = game_type
                self.set_trumps(game_type)
                self.play_caller = player
                # Tout
                if self.game_type in ('Solo-Eichel', 'Solo-Blatt', 'Solo-Herz', 'Solo-Schelle', 'Wenz'):
                    self.set_tout(self.play_caller)
                break

        # Make teams
        match self.game_type:
            case 'Rufspiel-Eichel' | 'Rufspiel-Blatt' | 'Rufspiel-Herz' | 'Rufspiel-Schelle':
                suit = self.game_type.split('-')[1]
                for player in self.players:
                    if player == self.play_caller or Card(suit, 'Ass') in player.hand:
                        self.playing_players.append(player)
                    else:
                        self.nonPlaying_players.append(player)

            case 'Solo-Eichel' | 'Solo-Blatt' | 'Solo-Herz' | 'Solo-Schelle' | 'Wenz':
                for player in self.players:
                    if player == self.play_caller:
                        self.playing_players.append(self.play_caller)
                    else:
                        self.nonPlaying_players.append(player)

        # Kontra and Re
        for player in self.nonPlaying_players:
            if not self.kontra_player:
                self.set_kontra(player)

        if self.kontra_player:
            self.set_re(self.play_caller)

        # Save laufende
        playing_players_cards = []
        nonPlaying_players_cards = []
        for player in self.playing_players:
            playing_players_cards.extend(player.hand)
        for player in self.nonPlaying_players:
            nonPlaying_players_cards.extend(player.hand)

        if self.trumps_in_order[-1] in playing_players_cards:
            hand_to_check = playing_players_cards
        else:
            hand_to_check = nonPlaying_players_cards

        count = 0
        for card in reversed(self.trumps_in_order):
            if card in hand_to_check:
                count += 1
            else:
                break

        if count >= 3 and self.game_type != 'Wenz':
            self.laufende = count
        elif self.game_type == 'Wenz' and count >= 2:
            self.laufende = count

        # Play tricks
        while self.current_trick_number < 8:
            self.play_trick()

        self.playing_team_score = sum(self.round_scores[player.name] for player in self.playing_players)
        self.nonPlaying_team_score = sum(self.round_scores[player.name] for player in self.nonPlaying_players)
