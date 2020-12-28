from random import randint

from computer_players.base_computer_player import BaseComputerPlayer
from dominion_game_engine.card_util import count_money
from dominion_game_engine.cards import *


class TheGuy(BaseComputerPlayer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.witches = 0
        self.militias = 0
        self.throne_rooms = 0
        self.moats = 0
        self.villages = 0
        self.silvers = 0
        self.golds = 0
        self.provinces = 0
        self.duchies = 0
        self.estates = 0

    def play_action_cards(self, hand):
        def has_card(card_class):
            return any(isinstance(c, card_class) for c in hand)

        def get_card(card_class):
            for card in hand:
                if isinstance(card, card_class):
                    return card
        for i in range(self.state.actions):
            if has_card(Witch) and self.state.supply['Curse'] > 0:
                self.play_card(get_card(Witch), hand)
            elif has_card(CouncilRoom):
                self.play_card(get_card(CouncilRoom), hand)
            elif has_card(Militia):
                self.play_card(get_card(Militia), hand)
            elif has_card(Moat):
                self.play_card(get_card(Moat), hand)

    def buy_stuff(self, hand):
        buys = self.state.buys

        for i in range(buys):
            money = count_money(hand + self.state.play_area, False) - self.state.used_money
            supply = self.state.supply

            if self.buy_card(money, 'Province'):
                self.provinces += 1
                break

            if self.buy_card(money, 'Gold'):
                self.golds += 1
                break

            if self.buy_card(money, 'Duchy', lambda: supply['Province'] < 4):
                self.duchies += 1
                break

            if self.buy_card(money, 'Witch', lambda: self.witches < 2):
                self.witches += 1
                break

            selector = randint(0, 5)
            if selector < 4:
                if self.buy_card(money, 'Festival'):
                    break
            elif selector == 4:
                if self.buy_card(money, 'Market'):
                    break
            elif selector == 5:
                if self.buy_card(money, 'CouncilRoom'):
                    break

            if self.buy_card(money, 'Militia', lambda: self.militias < 2):
                self.militias += 1
                break

            if self.buy_card(money, 'ThroneRoom', lambda: self.throne_rooms < 2):
                self.throne_rooms += 1
                break

            selector = randint(0, 5)
            if selector == 0 and self.villages < 2 and self.silvers > 2:
                if self.buy_card(money, 'Village'):
                    self.villages += 1
                    break
            else:
                if self.buy_card(money, 'Silver'):
                    self.silvers += 1
                    break

            if self.buy_card(money, 'Moat', lambda: self.moats < 3):
                self.moats += 1
                break

    def respond(self, request, *args):
        return
