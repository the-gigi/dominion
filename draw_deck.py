from card_stack import CardStack
from cards import Copper, Estate


class DrawDeck(CardStack):
    def __init__(self):
        CardStack.__init__(self, 7 * [Copper] + 3 * [Estate])

    def draw_new_hand(self):
        """Draw 5 cards  """

