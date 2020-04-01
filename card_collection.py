from cards import *


class CardStack:
    def __init__(self, cards=()):
        self.cards = list(cards)

    def shuffle(self):
        """Shuffle the cards in the collection and return the collection"""

        return self

    def draw_cards(self, n):
        """ """

    def peek(self, n):
        """Return a copy of the top n cards without removing them """

    def add_to_top(self, cards):
        """Add the cards to the top of the stack """

    def add_to_bottom(self, cards):
        """Add the cards to the bottom of the stack """

    @property
    def count(self):
        return len(self.cards)


