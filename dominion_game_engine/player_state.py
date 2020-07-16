import copy

from dominion_game_engine.card_stack import CardStack
from dominion_game_engine.cards import *
from dominion_game_engine.personal_state import PersonalState


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

        # How much money did the player used in the current turn
        self.used_money = 0

        self._personal_state = PersonalState(hand=copy.deepcopy(self.hand),
                                             discard_pile=copy.deepcopy(self.discard_pile),
                                             draw_deck=self.draw_deck.as_dict(),
                                             supply=copy.deepcopy(supply),
                                             play_area=[])

    def dump(self):
        print('Name:', self.name)
        print(self.hand)
        print(repr(self.discard_pile))
        print(repr(self.draw_deck))

    def _cleanup(self):
        """Discard hand and play area
        """
        self.discard_pile.add_to_top(self.hand + self.play_area)
        self.hand = []
        self.play_area = []

    def initialize_draw_deck(self):
        """Add 7 coppers and 3 estates to the draw deck and shuffle it"""
        for i in range(7):
            self.draw_deck.cards.append(Copper())
        for i in range(3):
            self.draw_deck.cards.append(Estate())
        self.draw_deck.shuffle()

    def reload_deck(self, n):
        if self.draw_deck.count < n:
            self.discard_pile.shuffle()
            self.draw_deck.cards += self.discard_pile.cards
            self.discard_pile = CardStack()

    def draw_cards(self, n):
        """Draw the top n cards from the draw deck and add them to the hand"""
        if n <= 0:
            return
        self.reload_deck(n)
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

    def get_personal_state(self, supply) -> PersonalState:
        return PersonalState(hand=copy.deepcopy(self.hand),
                             discard_pile=copy.deepcopy(self.discard_pile),
                             draw_deck=self.draw_deck.as_dict(),
                             supply=copy.deepcopy(supply),
                             play_area=self.play_area[:],
                             actions=self.actions,
                             buys=self.buys,
                             used_money=self.used_money)


    @property
    def personal_state(self):
        return self._personal_state
