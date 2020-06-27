from random import randint

from computer_players.base_computer_player import BaseComputerPlayer
from dominion.card_util import count_money
from dominion.cards import *

class TheGuy(BaseComputerPlayer):
    def play_action_cards(self, hand):
        for i in range(self.state.actions):
            for card in hand:
                if isinstance(card, CouncilRoom):
                    self.play_card(card, hand)
                elif isinstance(card, Militia):
                    self.play_card(card, hand)

    def buy_stuff(self, hand):
        buys = self.state.buys

        for i in range(buys):
            money = count_money(hand + self.state.play_area) - self.state.used_money
            supply = self.state.supply

            if self.buy_card(money, Province):
                break

            if self.buy_card(money, Gold):
                break

            if self.buy_card(money, Duchy, lambda: supply[Province] < 4):
                break

            if randint(0, 1) == 0:
                if self.buy_card(money, Festival):
                    break
            else:
                if self.buy_card(money, CouncilRoom):
                    break

            if self.buy_card(money, Militia):
                break

            if self.buy_card(money, Silver):
                break

    def respond(self, request, *args):
        return
