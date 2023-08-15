from itertools import combinations
from Game.GameClass import Game
import math
import random


# Iterative Round Robin Tournament
def round_robin_tournament(players):

    # Ensure there are a multiple of 4 players
    if len(players) % 4 != 0:
        raise ValueError("Number of players must be a multiple of 4 for this setup.")

    cumulative_scores = {player.name: 0 for player in players}

    # Generate all possible combinations of 4 players
    possible_matchups = list(combinations(players, 4))

    for group in possible_matchups:
        game = Game(5, list(group))
        _, scores = game.play_game()

        for player, score in scores.items():
            cumulative_scores[player] += score

    # Assign fitness based on normalized score
    fitness_scores = {}
    for player_name, score in cumulative_scores.items():
        genome_key = int(player_name.split(" ")[1])
        fitness_scores[genome_key] = score

    return fitness_scores  # Dict of {g.key: fitness_score}


# Iterative Knockout Tournament
def knockout_tournament(players):
    base_factor = 2
    num_players = len(players)

    # Ensure number of players is a power of 4
    if math.log(num_players, 4) % 1 != 0:
        raise ValueError("Number of players must be a power of 4 for this setup.")

    # Calculate the prize for the earliest eliminated players
    initial_prize = 100 / (base_factor * (2 * num_players - 1))

    current_players = players[:]
    fitness_scores = {}
    round_num = 0

    while len(current_players) > 1:
        groups = [current_players[i:i+4] for i in range(0, len(current_players), 4)]
        next_round_players = []
        eliminated_players = []

        for group in groups:
            game = Game(100, group)
            winner, _ = game.play_game()
            next_round_players.append(winner)
            eliminated_players.extend([player for player in group if player != winner])

        prize_for_this_round = initial_prize * (base_factor ** round_num)

        for player in eliminated_players:
            fitness_scores[int(player.name.split(" ")[1])] = prize_for_this_round

        current_players = next_round_players
        round_num += 1

    # Winner prize
    fitness_scores[int(current_players[0].name.split(" ")[1])] = initial_prize * (base_factor ** round_num)

    return fitness_scores  # Dict of {g.key: fitness_score}
