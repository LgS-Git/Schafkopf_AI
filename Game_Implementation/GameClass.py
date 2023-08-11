from PlayerClass import Player
from RoundClass import Round


class Game:

    def __init__(self, total_rounds):
        self.total_rounds = total_rounds

        self.players = [Player(f"Player {i + 1}") for i in range(4)]
        self.scores = {player.name: 0 for player in self.players}
        self.current_round = None
        self.current_round_number = 0

    def play_round(self, start_player_index):

        self.current_round = Round(self.players, start_player_index)
        round_scores = self.current_round.play_round()

        # After the round ends, update the total scores

    def play_game(self):
        while not self.current_round_number >= self.total_rounds:
            self.current_round_number += 1
            start_player_index = (self.current_round_number-1) % 4
            self.play_round(start_player_index)

        # This way, the AI tries to Win games, not win as much money as possible over a ton of games (Maybe a difference?)
        Winner = max(self.scores, key=self.scores.get)

        return Winner
