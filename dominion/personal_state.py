from dominion.card_util import *


class PersonalState:
    def __init__(self,
                 hand,
                 discard_pile,
                 draw_deck,
                 supply,
                 play_area,
                 actions=1,
                 buys=1,
                 used_money=0
                 ):
        """ """
        self.hand = hand
        self.discard_pile = discard_pile
        self.supply = supply
        self.draw_deck = draw_deck
        self.play_area = play_area
        self.actions = actions
        self.buys = buys
        self.used_money = used_money

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

