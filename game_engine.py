from collections import Sequence

import object_model


class GameEngine:
    def __init__(self, game: object_model.Game, players: Sequence):
        self.game_object = game
        self.players = players
        self.active_player_index = 0

    @property
    def game_over(self):
        """Returns the is_over property of the game object"""
        return self.game_object.is_over

    def find_winner(self):
        """The winner is the player with the most victory points

        In case of a tie the money is the tie breaker

        Returns the winning player
        """
        return self.game_object.find_winners()

    @property
    def active_player(self):
        """Return the current active player based on the self.active_player index

        """
        return self.players[self.active_player_index]

    def advance_player(self):
        self.active_player_index = (self.active_player_index + 1) % len(self.players)
        self.game_object.active_player_index = self.active_player_index

    def run(self):
        """This is the main loop of the game

        """
        while not self.game_over:
            self.active_player.play()
            self.game_object.end_turn()
            self.advance_player()

        winner = self.find_winner()
        print(f'{winner.name} won the game!!!')
