from card_util import *


class PersonalState:
    def __init__(self, hand, discard_pile, draw_deck, supply):
        """ """
        self.hand = hand
        self.discard_pile = discard_pile
        self.supply = supply
        self.draw_deck = draw_deck
        self.play_area = []

    @property
    def money(self):
        money = count_money(self.hand + self.discard_pile.cards)
        money += self.draw_deck['Copper'] + 2 * self.draw_deck['Silver'] + 3 * self.draw_deck['Gold']
        return money
