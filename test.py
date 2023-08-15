from Game.CardClass import Card
from NEAT.one_hot_functions import encode_game_state, encode_cards, encode_players, encode_game_type
import random

# Define a test


class Player:

    def __init__(self, name):
        self.name = name
        self.hand = []  # List of card objects, if Card is played, it is replaced by None

    def receive_cards(self, cards):
        self.hand.extend(cards)

    def count_cards_in_hand(self):
        return sum(1 for card in self.hand if card != None)


def test_encode_game_state():

    # Create dummy data
    cards = [Card(suit, rank) for suit in Card.SUITS for rank in Card.RANKS]
    random.shuffle(cards)

    players = [
        Player("Player 1"),
        Player("Player 2"),
        Player("Player 3"),
        Player("Player 4")
    ]

    for i, player in enumerate(players):
        player.receive_cards(cards[i*8:(i+1)*8])

    current_trick = [("Player 1", cards[0]), ("Player 2", cards[1]), ("Player 3", cards[2]), ("Player 4", cards[3])]
    tricks_per_player = {
        "Player 1": [cards[4:6], cards[8:10]],
        "Player 2": [cards[6:8]],
        "Player 3": [],
        "Player 4": [cards[10:12]]
    }
    start_player = players[0]
    round_scores = {"Player 1": 10, "Player 2": 20, "Player 3": 30, "Player 4": 40}
    game_scores = {"Player 1": 100, "Player 2": 200, "Player 3": 300, "Player 4": 400}
    kontra_player = players[1]
    re_player = players[2]
    tout_player = players[3]
    klopfen_players = [players[0], players[3]]
    game_type = 'Rufspiel-Eichel'

    # Test individual encoding functions
    cards_encoded = encode_cards(players[0], current_trick, tricks_per_player)
    print(f"encode_cards length: {len(cards_encoded)}")

    players_encoded = encode_players(players, start_player, round_scores, game_scores, kontra_player, re_player, tout_player, klopfen_players)
    print(f"encode_players length: {len(players_encoded)}")

    game_type_encoded = encode_game_type(game_type)
    print(f"encode_game_type length: {len(game_type_encoded)}")

    # Test encode_game_state
    encoded_state = encode_game_state(players[0], current_trick, tricks_per_player, players, start_player, round_scores,
                                      game_scores, kontra_player, re_player, tout_player, klopfen_players, game_type)
    assert len(encoded_state) == 321, f"Expected 321, but got {len(encoded_state)}"


test_encode_game_state()
