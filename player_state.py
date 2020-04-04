import copy

from card_stack import CardStack
from cards import *


class PlayerState:
    """The Player is a base class for the HumanPlayer and ComputerPlayer classes

    """

    def __init__(self, name):
        self.name = name
        self.hand = []
        self.draw_deck = CardStack()
        self.discard_pile = CardStack()

        # How many action cards can the player play
        self.actions = 1

        # How many cards can the player buy
        self.buy = 1

    def dump(self):
        print('Name:', self.name)
        self.hand.dump()

    def cleanup(self):
        """Discard hand and play area
        """

    def initialize_draw_deck(self):
        """Add 7 coppers and 3 estates to the draw deck and shuffle it"""

    def draw_new_hand(self):
        """Draw the 5 top cards from the draw deck and add them to the hand"""
        raise NotImplementedError

    def end_turn(self):
        """Perform the following:
            - cleanup
            - reset buys to 1
            - reset actions to 1
        """
        print('end turn')

    @property
    def personal_state(self):
        return dict(hand=copy.deepcopy(self.hand), discard_pile=copy.deepcopy(self.discard_pile))
