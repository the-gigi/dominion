from card_collection import CardCollection
from cards import Copper, Estate


class DrawDeck(CardCollection):
    def __init__(self):
        CardCollection.__init__(self, 7 * [Copper] + 3 * [Estate])

    def draw_new_hand(self):
        """Draw 5 cards  """

