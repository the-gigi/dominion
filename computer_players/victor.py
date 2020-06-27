from dominion.card_util import count_money
from dominion.object_model import BasePlayer
from dominion.cards import *


class Victor(BasePlayer):
    def play(self):
        """
        Victor only buys the largest possible victory card
        """
        hand = self.state.hand
        supply = self.state.supply
        money = count_money(hand) - self.state.used_money
        if supply[Province] > 0 and money >= Province.Cost:
            self.game_client.buy(Province)
        elif supply[Duchy] > 0 and money >= Duchy.Cost:
            self.game_client.buy(Duchy)
        elif supply[Estate] > 0 and money >= Estate.Cost:
            self.game_client.buy(Estate)

        self.game_client.done()

    def respond(self, request, *args):
        return
