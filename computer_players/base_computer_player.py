from card_util import count_money
from object_model import BasePlayer
from player_state import *


class BaseComputerPlayer(BasePlayer):
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

    def play_action_cards(self, hand):
        pass

    def buy_card(self, money, card_type, condition=lambda:True):
        if money >= card_type.Cost and self.personal_state.supply[card_type] > 0 and condition():
            ok = self.game_client.buy(card_type)
            return ok
            return True

        return False

    def buy(self, supply, money, buys):
        """This method should be implemented by derived classes

        """
        return False

    def buy_stuff(self, hand):
        while self.personal_state.buys > 0:
            buys = self.personal_state.buys
            supply = self.personal_state.supply
            money = count_money(hand + self.personal_state.play_area) - self.personal_state.used_money

            if self.buy(supply, money, buys):
                continue

            for card_type, condition in ((Province, lambda: True),
                                         (Gold, lambda: supply[Province] >= 4),
                                         (Duchy, lambda: supply[Province] < 4),
                                         (Silver, lambda: supply[Province] >= 4 or supply[Duchy] >= 4),
                                         (Estate, lambda: supply[Province] < 4 and supply[Duchy] < 4)):
                if self.buy_card(money, card_type, condition):
                    break

            # Can't byt anything interesting
            break

    def play_card(self, card, hand):
        self.game_client.play_action_card(card)
        hand.remove(card)

    def play(self):
        """
        """
        hand = self.personal_state.hand
        self.play_no_brainers(hand)
        self.play_action_cards(hand)
        self.buy_stuff(hand)
        self.game_client.done()

    def respond(self, request, *args):
        return
