from NEAT.one_hot_functions import encode_cards, encode_players
from Game.PlayerClass import Player
from Game.CardClass import Card

#### Test Card encoding ####

# Sample Card instances for testing
card1 = Card('Schelle', '7')
card2 = Card('Schelle', '8')
card3 = Card('Schelle', '9')
card4 = Card('Schelle', 'König')
card5 = Card('Schelle', '10')
card6 = Card('Schelle', 'Ass')
card7 = Card('Schelle', 'Unter')
card8 = Card('Schelle', 'Ober')

# Sample Player instance with a hand containing some cards
player_test = Player('Player 1')
player_test.hand = [card1, card2, card3, card4]

# Sample current_trick list with player names and their played cards
current_trick_test = [('Player 1', card5), ('Player 2', card6)]

# Sample tricks_per_player dictionary
tricks_per_player_test = {
    'Player 1': [],
    'Player 2': [(card7, card8, card3, card4)],  # One trick with 4 cards
    'Player 3': [],
    'Player 4': []
}

# Testing the function
encoded_cards = encode_cards(player_test, current_trick_test, tricks_per_player_test)


###### Test Player encoding ######

# 1. Sample Player instances with mock data
player1 = Player('Player 1')
player1.hand = [Card('Schelle', '7'), Card('Schelle', '8')]

player2 = Player('Player 2')
player2.hand = [Card('Schelle', '9'), Card('Schelle', 'König')]

player3 = Player('Player 3')
player3.hand = [Card('Schelle', '10'), Card('Schelle', 'Ass')]

player4 = Player('Player 4')
player4.hand = [Card('Schelle', 'Unter'), Card('Schelle', 'Ober')]

players = [player1, player2, player3, player4]

# 2. Mock data for scores
round_scores = {
    'Player 1': 30,
    'Player 2': 20,
    'Player 3': 50,
    'Player 4': 20
}

game_scores = {
    'Player 1': 120,
    'Player 2': 100,
    'Player 3': 110,
    'Player 4': 90
}

# 3. Mock data for decisions
klopfen_players = [player1, player2]
kontra_players = player1
re_player = player2
tout_player = None

# 4. Mock start player
start_player = player2

# Testing the function
encoded_state = encode_players(players, start_player, round_scores, game_scores, kontra_players, re_player, tout_player, klopfen_players)
print(encoded_state)

