from card_collection import CardCollection
from cards import Copper, Estate


class Hand(CardCollection):
    def __init__(self):
        CardCollection.__init__(self, 7 * [Copper] + 3 * [Estate])
