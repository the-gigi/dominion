from typing import List
from cards import BaseCard


class CardCollection:
    def __init__(self, cards=()):
        self.cards = list(cards)

    def shuffle(self):
        """Shuffle the cards in the collection and return the collection"""

        return self

    def draw_cards(self, n):
        """ """

    def peak_cards(self, n):
        """ """

    def add_on_top(self, cards):
        """ """

    def add_to_bottom(self, cards):
        """ """

    @property
    def count(self):
        return len(self.cards)
