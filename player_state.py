import copy

from card_stack import CardStack
from cards import *
from personal_state import PersonalState


class PlayerState:
    """The Player is a base class for the HumanPlayer and ComputerPlayer classes

    """

    def __init__(self, name, supply):
        self.name = name
        self.hand = []
        self.play_area = []
        self.draw_deck = CardStack()
        self.discard_pile = CardStack()
        self.initialize_draw_deck()
        self.draw_cards(5)

        # How many action cards can the player play
        self.actions = 1

        # How many cards can the player buy
        self.buys = 1

        self._personal_state = PersonalState(hand=copy.deepcopy(self.hand),
                                             discard_pile=copy.deepcopy(self.discard_pile),
                                             draw_deck=self.draw_deck.as_dict(),
                                             supply=copy.deepcopy(supply))

    def dump(self):
        print('Name:', self.name)
        print(self.hand)
        print(repr(self.discard_pile))
        print(repr(self.draw_deck))

    def _cleanup(self):
        """Discard hand and play area
        """
        self.discard_pile.add_to_top(self.hand)
        self.hand = []

    def initialize_draw_deck(self):
        """Add 7 coppers and 3 estates to the draw deck and shuffle it"""
        self.draw_deck.cards = [Copper()] * 7 + [Estate()] * 3
        self.draw_deck.shuffle()

    def draw_cards(self, n):
        """Draw the top n cards from the draw deck and add them to the hand"""
        if n <= 0:
            return
        if self.draw_deck.count < n:
            self.discard_pile.shuffle()
            self.draw_deck.cards += self.discard_pile.cards
            self.discard_pile = CardStack()
            if self.draw_deck.count < n:
                n = self.draw_deck.count
        self.hand += self.draw_deck.pop(n)

    def done(self):
        """Perform the following:
            - cleanup
            - reset buys to 1
            - reset actions to 1
        """
        self._cleanup()
        self.draw_cards(5)
        self.buys = 1
        self.actions = 1
        print(f'{self.name}: done')

    def sync_personal_state(self, supply):
        self.personal_state.discard_pile = CardStack(self.discard_pile.cards[:])
        self.personal_state.hand = self.hand[:]
        self.personal_state.draw_deck = self.draw_deck.as_dict()
        self.personal_state.supply = supply
        self.personal_state.play_area = self.play_area[:]
        self.personal_state.actions = self.actions
        self.personal_state.buys = self.buys

    @property
    def personal_state(self):
        return self._personal_state
