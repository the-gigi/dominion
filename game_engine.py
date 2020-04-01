from cards import Copper, Estate

copper_count = 60
silver_count = 40
gold_count = 30


class GameEngine:
    def __init__(self, players, card_types):
        self.players = players
        self.active_player = 0

        self.piles = {c: 13 for c in card_types}

        self.piles[Copper] = copper_count - len(players) * 7
        # self.piles[Silver] = silver_count
        # self.piles[Gold] = silver_count

        self.piles[Estate] = 8 if len(players) == 2 else 12
        # self.piles[Duchy] = 8 if len(players) == 2 else 12
        # self.piles[Province] = 8 if len(players) == 2 else 12
        # self.piles[Curse] = (len(players) - 1) * 10

    @property
    def game_over(self):
        """Check if all provinces are gone or 3 supply piles are empty

        return True if the game is over and False otherwise
        """

    def count_player_points(self, player):
        """Count the total victory points in
           the player's hand, deck and discard pile

           return the number of victory points
        """

    def count_player_money(self, player):
        """Count the total amount of coins in
           the player's hand, deck and discard pile

           return the sum of all the coins
        """

    def find_winner(self, players):
        """The winner is the player with the most victory points

        In case of a tie the money is the tie breaker

        Return the name of the winning player
        """

    def is_pile_empty(self, card_type):
        """Check if a card pile is empty
        """

    def get_active_player(self):
        """Return the current active player based on the self.active_player index

        """

    def finish_turn(self):
        """Perform this operation at the end of turn

        - call cleanup() on the active  player
        - update the active player index to the next player
        """

    def run(self):
        """This is the main loop of the game"""
        while not self.game_over:
            player = self.active_player
            action = player.play()
