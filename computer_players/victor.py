from card_util import count_money
from object_model import BasePlayer
from cards import *


class Victor(BasePlayer):
    def play(self):
        """
        Victor only buys the largest possible victory card
        """
        hand = self.personal_state.hand
        supply = self.personal_state.supply
        money = count_money(hand) - self.personal_state.used_money
        if supply[Province] > 0 and money >= Province.Cost:
            self.game_client.buy(Province)
        elif supply[Duchy] > 0 and money >= Duchy.Cost:
            self.game_client.buy(Duchy)
        elif supply[Estate] > 0 and money >= Estate.Cost:
            self.game_client.buy(Estate)

        self.game_client.done()

    def respond(self, request, *args):
        return
