from object_model import BasePlayer
from card_util import count_money
from cards import *


class Rockefeller(BasePlayer):
    def play(self):
        """Rockefeller buys as many treasures as possible. that's it!!!!

        it checks how much money it's got in hand
        buys the largest treasure it can
        ends the turn
        """

        hand = self.game_client.personal_state.hand
        money = count_money(hand)
        if money >= Gold.Cost:
            self.game_client.buy(Gold)
        elif money >= Silver.Cost:
            self.game_client.buy(Silver)
        elif money >= Copper.Cost:
            self.game_client.buy(Copper)

        self.game_client.done()

    def react(self, attack):
        return False
