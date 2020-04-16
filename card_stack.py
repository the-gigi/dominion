from collections import defaultdict
import random

import card_util
from cards import *


class CardStack:
    def __init__(self, cards=()):
        self.cards = list(cards)

    def shuffle(self):
        """Shuffle the cards in the stack and return the stack"""
        random.shuffle(self.cards)

    def pop(self, n):
        """Take n cards from the top of the deck and return them"""
        cards = self.peek(n)
        self.cards = self.cards[n:]
        return cards

    def peek(self, n):
        """Return a copy of the top n cards without removing them

        If n is greater than the number of cards raise a RuntimeError
        """
        if n > len(self.cards):
            raise RuntimeError(f'There are only {len(self.cards)} cards in the stack.')
        return self.cards[:n]

    def add_to_top(self, cards):
        """Add the cards to the top of the stack """
        self.cards = cards + self.cards

    def add_to_bottom(self, cards):
        """Add the cards to the bottom of the stack """
        self.cards += cards

    @property
    def count(self):
        return len(self.cards)

    def __eq__(self, other):
        """
        store the dict repr of self in a var
        store the dict repr of other in a var
        return the comparison of the two vars
        """
        return self.as_dict() == other.as_dict()

    def as_dict(self):
        return card_util.as_dict(self.cards)

    def __repr__(self):
        return str(self.as_dict())
