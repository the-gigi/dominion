from dominion.card_util import *


class PersonalState:
    def __init__(self, hand, discard_pile, draw_deck, supply):
        """ """
        self.hand = hand
        self.discard_pile = discard_pile
        self.supply = supply
        self.draw_deck = draw_deck
        self.play_area = []
        self.actions = 1
        self.buys = 1
        self.used_money = 0

    @property
    def money(self):
        money = count_money(self.hand + self.discard_pile.cards)
        money += self.draw_deck['Copper'] + 2 * self.draw_deck['Silver'] + 3 * self.draw_deck['Gold']
        return money

    @property
    def points(self):
        points = count_points(self.hand + self.play_area + self.discard_pile.cards)
        points += self.draw_deck['Estate'] + 3 * self.draw_deck['Duchy'] + 6 * self.draw_deck['Province']
        return points

