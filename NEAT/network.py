import neat
import pickle
import numpy as np
from Game.PlayerClass import Player
from .tournaments import round_robin_tournament, knockout_tournament


def eval_genomes(genomes, config):
    nets = []
    players = []
    genome_dict = {}

    # Create network for all genomes in population and assign to players
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        player_name = f"Player {genome.key}"  # Using genome key as a unique identifier
        players.append(Player(player_name, net))
        genome_dict[genome_id] = genome

    # Play tournament (All tournaments should give out: {g.key: fitness_score})
    fitness_scores = knockout_tournament(players)

    # Assign fitness scores
    for genome_key, fitness in fitness_scores.items():
        genome_dict[genome_key].fitness = fitness


def save_genomes(genomes, filename):
    with open(filename, 'wb') as f:
        pickle.dump(genomes, f)


def decide_card_to_play(network_output, player, valid_cards_mask):

    # Choose the card with the highest probability after mask
    masked_output = network_output[:8]
    for idx, value in enumerate(valid_cards_mask):
        if value == -1:
            masked_output[idx] = -1
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
    print(possible_game_types)
    masked_network_output = network_output[12:]
    for idx, game_type in enumerate(all_game_types):
        if game_type not in possible_game_types:
            masked_network_output[idx] = -1
    print(masked_network_output)
    chosen_index = np.argmax(masked_network_output)
    game_type = all_game_types[chosen_index]
    return game_type
