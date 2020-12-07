import random
from typing import List

from dominion_game_engine import card_util
from dominion_game_engine.cards import BaseCard


class CardStack:
    def __init__(self, cards=()):
        self.cards = list(cards)

    def invariant(self):
        # Verifies that there are only unique cards in a stack of cards (no copies of cards).
        assert(len(self.cards) == len(set(self.cards)))

    def shuffle(self):
        """Shuffle the cards in the stack and return the stack"""
        random.shuffle(self.cards)
        self.invariant()

    def pop(self, n):
        """Take n cards from the top of the deck and return them"""
        cards = self.peek(n)
        self.cards = self.cards[n:]
        self.invariant()
        return cards

    def peek(self, n):
        """Return a copy of the top n cards without removing them

        If n is greater than the number of cards raise a RuntimeError
        """
        self.invariant()
        if n > len(self.cards):
            raise RuntimeError(f'There is/are only {len(self.cards)} card(s) in the stack.')
        self.invariant()
        return self.cards[:n]

    def add_to_top(self, cards: List[BaseCard]):
        """Add the cards to the top of the stack """
        self.invariant()
        self.cards = cards + self.cards
        self.invariant()

    def add_to_bottom(self, cards: List[BaseCard]):
        """Add the cards to the bottom of the stack """
        self.invariant()
        self.cards += cards
        self.invariant()

    @property
    def count(self) -> int:
        return len(self.cards)

    def __eq__(self, other):
        """
        store the dict repr of self in a var
        store the dict repr of other in a var
        return the comparison of the two vars
        """
        d1 = self.as_dict()
        d2 = other.as_dict()
        return d1 == d2

    def as_dict(self):
        return card_util.as_dict(self.cards)

    def __repr__(self):
        return str(self.as_dict())
