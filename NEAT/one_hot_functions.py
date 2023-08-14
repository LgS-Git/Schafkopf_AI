from Game.CardClass import Card


def encode_cards(player, current_trick, tricks_per_player):
    all_cards = [Card(suit, rank) for suit in Card.SUITS for rank in Card.RANKS]

    encoding = []

    for card in all_cards:
        # Check the position of the card and encode accordingly
        if card in player.hand:
            encoding.extend([1, 0, 0, 0, 0, 0, 0])
        elif card in current_trick[1]:
            encoding.extend([0, 1, 0, 0, 0, 0, 0])
        else:
            # Check if the card is in any player's won tricks
            found = False
            for player_name, tricks in tricks_per_player.items():
                for trick in tricks:
                    if card in trick:
                        player_idx = int(player_name[-1])
                        encoding.extend([0] * (player_idx + 1) + [1] + [0] * (6 - player_idx))
                        found = True
                        break
                if found:
                    break
            if not found:
                # Card is hidden
                encoding.extend([0, 0, 0, 0, 0, 0, 1])

    return encoding


def encode_players(players, start_player, round_scores, game_scores, kontra_player, re_player, tout_player, klopfen_players):

    ## Warning ##
    # Scores are not one_hot encoded, since I'm not sure how and binary encoding changes the width
    # I hope its ok, since only scores are not one_hot and they are target values
    # If it performs badly, try only the game_score (score that should be maximized), the round_score is implicitly known anyway

    def player_encoding(player):
        # Absolute Position
        absolute_position = [0, 0, 0, 0]
        absolute_position[int(player.name[-1]) - 1] = 1

        # Relative Position
        relative_position = [0, 0, 0, 0]
        start_idx = int(start_player.name[-1]) - 1
        current_idx = int(player.name[-1]) - 1
        relative_idx = (current_idx - start_idx) % 4
        relative_position[relative_idx] = 1

        # Number of cards in hand
        cards_in_hand = [1] * player.count_cards_in_hand() + [0] * (8 - player.count_cards_in_hand)

        # Round score
        round_score = [round_scores[player.name]]

        # Game score
        game_score = [game_scores[player.name]]

        # Decisions markers
        decisions = [
            1 if player in klopfen_players else 0,
            1 if tout_player == player else 0,
            1 if kontra_player == player else 0,
            1 if re_player == player else 0,
        ]

        return absolute_position + relative_position + cards_in_hand + round_score + game_score + decisions

    encoding = []
    for player in players:
        encoding.extend(player_encoding(player))

    return encoding


def encode_game_type(game_type):

    game_types = ['Rufspiel-Eichel', 'Rufspiel-Blatt', 'Rufspiel-Herz', 'Rufspiel-Schelle',
                  'Solo-Eichel', 'Solo-Blatt', 'Solo-Herz', 'Solo-Schelle', 'Wenz']

    encoding = [0] * len(game_types)
    if game_type in game_types:
        encoding[game_types.index(game_type)] = 1

    return encoding


def encode_game_state(player, current_trick, tricks_per_player, players, start_player, round_scores, game_scores, kontra_player, re_player, tout_player, klopfen_players, game_type):
    return encode_cards(player, current_trick, tricks_per_player) + encode_players(players, start_player, round_scores, game_scores, kontra_player, re_player, tout_player, klopfen_players) + encode_game_type(game_type)
