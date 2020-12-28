from collections import Counter
from random import randint

from computer_players.base_computer_player import BaseComputerPlayer
from dominion_game_engine.card_util import count_money
from dominion_game_engine.cards import *


class TheGuy(BaseComputerPlayer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.card_counter = Counter()

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

            if has_card(Bandit):
                self.play_card(get_card(Bandit), hand)
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
                self.card_counter['Province'] += 1
                break

            if self.buy_card(money, 'Gold'):
                self.card_counter['Gold'] += 1
                break

            if self.buy_card(money, 'Duchy', lambda: supply['Province'] < 4):
                self.card_counter['Duchy'] += 1
                break

            if self.buy_card(money, 'Witch', lambda: self.card_counter['Witch'] < 2):
                self.card_counter['Witch'] += 1
                break

            if self.buy_card(money, 'Bandit', lambda: self.card_counter['Bandit'] < 2):
                self.card_counter['Bandit'] += 1
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

            if self.buy_card(money, 'Militia', lambda: self.card_counter['Militia'] < 2):
                self.card_counter['Militia'] += 1
                break

            if self.buy_card(money, 'ThroneRoom', lambda: self.card_counter['ThroneRoom'] < 1):
                self.card_counter['ThroneRoom'] += 1
                break

            selector = randint(0, 5)
            if selector == 0 and self.card_counter['Village'] < 2 and self.card_counter['Silver'] > 2:
                if self.buy_card(money, 'Village'):
                    self.card_counter['Village'] += 1
                    break
            else:
                if self.buy_card(money, 'Silver'):
                    self.card_counter['Silver'] += 1
                    break

            if self.buy_card(money, 'Moat', lambda: self.card_counter['Moat'] < 2):
                self.card_counter['Moat'] += 1
                break

    def respond(self, request, *args):
        return
