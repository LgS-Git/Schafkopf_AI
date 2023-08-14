import neat
import pickle
import numpy as np
from Game.GameClass import Game
from Game.PlayerClass import Player
from itertools import combinations


# Iterative Round Robin Tournament
def round_robin_tournament(players):
    # Ensure there are a multiple of 4 players
    if len(players) % 4 != 0:
        raise ValueError("Number of players must be a multiple of 4 for this setup.")

    cumulative_scores = {player.name: 0 for player in players}

    # Generate all possible combinations of 4 players
    possible_matchups = list(combinations(players, 4))

    for group in possible_matchups:
        game = Game(10000, list(group))
        _, scores = game.play_game()

        for player, score in scores.items():
            cumulative_scores[player] += score

    # Assign fitness based on normalized score
    fitness_scores = {}
    for player_name, score in cumulative_scores.items():
        genome_key = int(player_name.split(":")[0])
        fitness_scores[genome_key] = score

    return fitness_scores  # Dict of {g.key: fitness_score}


def eval_genomes(genomes, config):
    nets = []
    players = []
    # Create network for all genomes in population and assign to players
    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        player_name = f"{g.key}:Player 1"  # Using genome key as a unique identifier
        players.append(Player(player_name, net))

    # Play tournament (All tournaments should give out: {g.key: fitness_score})
    fitness_scores = round_robin_tournament(players)

    # Assign fitness scores
    for genome_key, fitness in fitness_scores.items():
        genomes[genome_key][1].fitness = fitness


def save_genomes(genomes, filename):
    with open(filename, 'wb') as f:
        pickle.dump(genomes, f)


# Load NEAT configuration
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     'neat_config.txt')

# Create the population
p = neat.Population(config)

# Add reporters for stats
p.add_reporter(neat.StdOutReporter(True))
stats = neat.StatisticsReporter()
p.add_reporter(stats)

# Run NEAT
winner = p.run(eval_genomes, 10)  # 50 generations as an example

save_genomes(winner, 'genomes/winner.pkl')
save_genomes(p, 'genomes/fittest_pop.pkl')


def decide_card_to_play(network_output, player, current_trick, trumps_in_order):
    # Determining suit or trump restriction if not first
    if len(current_trick) > 0:
        # Determine the leading card suit or trump
        leading_suit = None
        leading_trump = False
        leading_card = current_trick[0][1]
        if leading_card not in trumps_in_order:
            leading_suit = leading_card.suit
        else:
            leading_trump = True

        # Check if leading_suit or trump in Hand
        has_matching_suit = False
        has_trump = False
        for card in player.hand:
            if card:
                if card.suit == leading_suit and card not in trumps_in_order:
                    has_matching_suit = True
                if card in trumps_in_order:
                    has_trump = True

    # Create a mask for valid plays
    mask = np.ones(8)
    for idx, card in enumerate(player.hand):
        if not card:
            mask[idx] = 0
        elif leading_suit:
            if has_matching_suit and card.suit != leading_suit:
                mask[idx] = 0
        elif leading_trump:
            if has_trump and card not in trumps_in_order:
                mask[idx] = 0

    # Choose the card with the highest probability after mask
    masked_output = network_output[:8] * mask
    chosen_index = np.argmax(masked_output)
    chosen_card = player.hand[chosen_index]

    return chosen_card


def decide_klopfen(network_output):
    if network_output[8] >= 0.5:
        return True
    return False


def decide_tout(network_output):
    if network_output[9] >= 0.5:
        return True
    return False


def decide_kontra(network_output):
    if network_output[10] >= 0.5:
        return True
    return False


def decide_re(network_output):
    if network_output[11] >= 0.5:
        return True
    return False


def decide_game_type(network_output, possible_game_types):
    all_game_types = ['Rufspiel-Eichel', 'Rufspiel-Blatt', 'Rufspiel-Herz', 'Rufspiel-Schelle',
                      'Solo-Eichel', 'Solo-Blatt', 'Solo-Herz', 'Solo-Schelle', 'Wenz', 'Passen']
    mask = np.ones(10)
    for idx, game_type in enumerate(all_game_types):
        if game_type != possible_game_types:
            mask[idx] = 0

    chosen_index = np.argmax(network_output[11:])
    game_type = all_game_types[chosen_index]
    return game_type
