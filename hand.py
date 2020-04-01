from card_collection import CardStack
from cards import Copper, Estate


class Hand(CardStack):
    def __init__(self):
        CardStack.__init__(self, 7 * [Copper] + 3 * [Estate])
