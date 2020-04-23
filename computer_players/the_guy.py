from card_util import count_money
from object_model import BasePlayer
from cards import *
from player_state import *


class TheGuy(BasePlayer):
    def play_no_brainers(self, hand):
        play = self.game_client.play_action_card
        to_remove = []
        for card in hand:
            if isinstance(card, Village):
                play(card)
                to_remove.append(card)
            elif isinstance(card, Festival):
                play(card)
                to_remove.append(card)
        for card in to_remove:
            hand.remove(card)

    def play_brainers(self, hand):
        for i in range(self.personal_state.actions):
            for card in hand:
                if isinstance(card, CouncilRoom):
                    self.play_card(card, hand)

    def buy_stuff(self, hand):
        buys = self.personal_state.buys
        buy = self.game_client.buy
        money = count_money(hand + self.personal_state.play_area)
        supply = self.personal_state.supply
        for i in range(buys):
            if money >= 8 and supply[Province] > 0:
                buy(Province)
            elif money >= 6 and supply[Gold] > 0:
                buy(Gold)
            elif money >= 5:
                if supply[Duchy] > 0 and supply[Province] < 4:
                    buy(Duchy)
                elif supply[Festival] > 0:
                    buy(Festival)
                elif supply[CouncilRoom] > 0:
                    buy(CouncilRoom)
            elif money >= 3 and supply[Silver] > 0:
                buy(Silver)

    def play_card(self, card, hand):
        self.game_client.play_action_card(card)
        hand.remove(card)

    def play(self):
        """
        Victor only buys the largest possible victory card
        """
        hand = self.personal_state.hand
        supply = self.personal_state.supply
        money = count_money(hand)

        self.play_no_brainers(hand)

        self.play_brainers(hand)

        self.buy_stuff(hand)

        self.game_client.done()

        supply = self.personal_state.supply
        print(f'points: {self.personal_state.points}')
        print(f'supply - provinces: {supply[Province]}, duchies: {supply[Duchy]}, estates: {supply[Estate]},')
        print('-' * 20)

    def respond(self, request):
        return

