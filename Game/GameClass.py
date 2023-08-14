from .RoundClass import Round


class Game:

    def __init__(self, total_rounds, list_of_players):
        self.total_rounds = total_rounds

        self.players = list_of_players
        self.scores = {player.name: [] for player in self.players}
        self.cumulative_score = {player.name: 0 for player in self.players}
        self.current_round = None
        self.current_round_number = 0
        self.round_storage = []

    def do_round(self, start_player_index):
        # Play and safe round
        self.current_round = Round(self.players, start_player_index, self.cumulative_score)
        self.current_round.play_round()
        self.round_storage.append(self.current_round)

        # Calc winners and points
        schneider = False
        schwarz = False
        tout = True if self.current_round.tout_player else False
        if not tout and (self.current_round.playing_team_score <= 30 or self.current_round.nonPlaying_team_score <= 30):
            schneider = True
        if not tout and (self.current_round.playing_team_score == 0 or self.current_round.nonPlaying_team_score == 0):
            schwarz = True
        laufende = self.current_round.laufende
        klopfen = len(self.current_round.klopfen_players)
        kontra = True if self.current_round.kontra_player else False
        re = True if self.current_round.re_player else False

        # Tarifs: Schneider/Laufende, Rufspiel, Solo
        tarif = [10, 20, 50]

        tarif_operations_in_order = [
            # Schneider
            {'condition': lambda: schneider, 'operation': lambda val: val + tarif[0]},
            # Schwarz
            {'condition': lambda: schwarz, 'operation': lambda val: val + tarif[0]},
            # Laufende
            {'condition': lambda: laufende > 0, 'operation': lambda val: val + (laufende*tarif[0])},
            # Klopfen
            {'condition': lambda: klopfen > 0, 'operation': lambda val: val * (2**klopfen)},
            # Kontra
            {'condition': lambda: kontra, 'operation': lambda val: val * 2},
            # Re
            {'condition': lambda: re, 'operation': lambda val: val * 2},
            # Tout
            {'condition': lambda: tout, 'operation': lambda val: val * 2},
        ]

        if self.current_round.game_type in ('Solo-Eichel', 'Solo-Blatt', 'Solo-Herz', 'Solo-Schelle', 'Wenz'):
            game_value = tarif[2]
            for op in tarif_operations_in_order:
                if op['condition']():
                    game_value = op['operation'](game_value)

            if (not tout and self.current_round.playing_team_score > 60) or (tout and self.current_round.playing_team_score == 120):
                self.scores[self.current_round.play_caller.name].append(game_value*3)
                for player in self.current_round.nonPlaying_players:
                    self.scores[player.name].append(-game_value)
            else:
                self.scores[self.current_round.play_caller.name].append(-game_value*3)
                for player in self.current_round.nonPlaying_players:
                    self.scores[player.name].append(game_value)
        else:
            game_value = tarif[1]
            for op in tarif_operations_in_order:
                if op['condition']():
                    game_value = op['operation'](game_value)

            if self.current_round.playing_team_score > 60:
                for player in self.current_round.playing_players:
                    self.scores[player.name].append(game_value)
                for player in self.current_round.nonPlaying_players:
                    self.scores[player.name].append(-game_value)
            else:
                for player in self.current_round.playing_players:
                    self.scores[player.name].append(-game_value)
                for player in self.current_round.nonPlaying_players:
                    self.scores[player.name].append(game_value)

    def play_game(self):
        while not self.current_round_number >= self.total_rounds:
            self.current_round_number += 1
            start_player_index = (self.current_round_number-1) % 4
            self.do_round(start_player_index)

        # Sum scores
        for player, scores in self.scores.items():
            self.cumulative_score[player] = sum(scores)

        # This way, the AI tries to Win games, not win as much money as possible over a ton of games (Maybe a difference?)
        Winner = max(self.cumulative_score, key=self.cumulative_score.get)

        return Winner, self.cumulative_score
