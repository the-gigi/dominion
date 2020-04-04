from cards import *


class GameEngine:
    def __init__(self, game, players):
        self.game = game
        self.players = players
        self.active_player_index = 0

    @property
    def game_over(self):
        """Returns the is_over property of the game object"""
        return self.game.is_over

    def count_player_points(self, player):
        """Count the total victory points in
           the player's hand, deck and discard pile

           return the number of victory points
        """
        raise NotImplementedError

    def count_player_money(self, player):
        """Count the total amount of coins in
           the player's hand, deck and discard pile

           return the sum of all the coins
        """
        raise NotImplementedError

    def find_winner(self):
        """The winner is the player with the most victory points

        In case of a tie the money is the tie breaker

        Returns the winning player
        """
        return self.game.find_winner()

    def finish_turn(self):
        """Perform this operation at the end of turn

        - call cleanup() on the active  player
        - update the active player index to the next player
        """
        raise NotImplemented

    @property
    def active_player(self):
        """Return the current active player based on the self.active_player index

        """
        return self.players[self.active_player_index]

    def advance_player(self):
        self.active_player_index = (self.active_player_index + 1) % len(self.players)
        self.game.active_player_index = self.active_player_index

    def run(self):
        """This is the main loop of the game

        """
        while not self.game_over:
            self.active_player.play(self.game, self.game.personal_player_state)
            self.game.end_turn()
            self.advance_player()

        winner = self.find_winner()
        print(f'{winner.name} won the game!!!')
