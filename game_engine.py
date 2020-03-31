from cards import Copper, Estate

copper_count = 60
silver_count = 40
gold_count = 30


class GameEngine:
    def __init__(self, players, card_types):
        self.piles = {c: 13 for c in card_types}

        self.piles[Copper] = copper_count - len(players) * 7
        #self.piles[Silver] = silver_count
        #self.piles[Gold] = silver_count

        self.piles[Estate] = 8 if len(players) == 2 else 12
        # self.piles[Duchie] = 8 if len(players) == 2 else 12
        # self.piles[Province] = 8 if len(players) == 2 else 12
        # self.piles[Curse] = (len(players) - 1) * 10

    def is_game_over(self):
        """Check if all provinces are gone or enough piles are empty

        in a 2 player game if 3 piles are empty the game is over
        in a 3/4 player if 2 piles are empty the game is over

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