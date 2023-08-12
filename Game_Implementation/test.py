from GameClass import Game
from CardClass import Card

'''
test_game = Game(2)

test_game.play_round(0)

test_game.current_round.set_game_type('Player 1', 'Wenz')

print(test_game.current_round.trumps_in_order)

trick_cards = [
    Card("Eichel", "10"),
    Card("Blatt", "Unter"),
    Card("Herz", "10"),
    Card("Eichel", "Ass")
]

for card in trick_cards:
    test_game.current_round.play_next_card(card)

winner, trick = test_game.current_round.determine_trick_winner()
print(f"The winner of the trick is: {winner.name}")
print(f'The winner won {trick}')
'''

test_game = Game(1000)

test_game.play_game()

print(test_game.current_round.game_type)
print(test_game.current_round.play_caller)
print(test_game.current_round.starting_hand)
print(len(test_game.scores['Player 1']))
print(test_game.final_score)
print(test_game.current_round.tricks_per_player)
print(test_game.current_round.round_scores)

print('Breakpoint')
