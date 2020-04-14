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
        supply = self.game_client.personal_state.supply
        money = count_money(hand)
        if supply[Gold] > 0 and money >= Gold.Cost:
            self.game_client.buy(Gold)
        elif supply[Silver] > 0 and money >= Silver.Cost:
            self.game_client.buy(Silver)
        elif supply[Copper] > 0 and money >= Copper.Cost:
            self.game_client.buy(Copper)

        self.game_client.done()

        supply = self.game_client.personal_state.supply
        print(f'money: {self.game_client.personal_state.money}')
        print(f'supply - gold: {supply[Gold]}, silver: {supply[Silver]}, copper: {supply[Copper]},')
        print('-' * 20)


    def react(self, attack):
        return False
