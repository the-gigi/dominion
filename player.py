from card_collection import CardCollection
from cards import *


class Player:
    """The Player is a base class for the HumanPlayer and ComputerPlayer classes

    """

    def __init__(self, name):
        self.Name = name
        self.hand = CardCollection()
        self.draw_deck = CardCollection()
        self.discard_pile = CardCollection()

    def dump(self):
        print('Name:', self.name)
        self.hand.dump()

    def cleanup(self):
        """ """

    def initialize_draw_deck(self):
        """Add 7 coppers and 3 estates to the draw deck and shuffle it"""

    def draw_new_hand(self):
        """Draw the 5 top cards from the draw deck and add them to the hand"""

    def end_turn(self):
        """Cleanup and  """

    def play(self, game):
        """The player has to make one of the actions on the game object

        Some actions are:
        - play card from hand
        - buy cards from thh piles
        - end turn

        If an invalid action is attempted the game object will return an error and wait

        """
        raise NotImplementedError