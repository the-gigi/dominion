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
        self.initialize_draw_deck()
        self.draw_new_hand()

        # How many action cards can the player play
        self.actions = 1

        # How many cards can the player buy
        self.buys = 1

    def dump(self):
        print('Name:', self.name)
        print(self.hand)

    def cleanup(self):
        """Discard hand and play area
        """

    def initialize_draw_deck(self):
        """Add 7 coppers and 3 estates to the draw deck and shuffle it"""
        self.draw_deck.cards = [Copper()] * 7 + [Estate()] * 3
        self.draw_deck.shuffle()

    def draw_new_hand(self):
        """Draw the 5 top cards from the draw deck and add them to the hand"""
        self.draw_deck.shuffle()
        self.hand = self.draw_deck.pop(5)

    def done(self):
        """Perform the following:
            - cleanup
            - reset buys to 1
            - reset actions to 1
        """
        print(f'{self.name}: done')

    @property
    def personal_state(self):
        return dict(hand=copy.deepcopy(self.hand), discard_pile=copy.deepcopy(self.discard_pile))
