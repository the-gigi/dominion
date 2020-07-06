from dominion.card_util import count_money, get_card_class
from dominion.cards import *
from dominion.object_model import BasePlayer


class BaseComputerPlayer(BasePlayer):
    def play_no_brainers(self, hand):
        play = self.game_client.play_action_card
        to_remove = []
        for card in hand:
            if isinstance(card, Village):
                play(card.Name())
                to_remove.append(card)
            elif isinstance(card, Festival):
                play(card.Name())
                to_remove.append(card)
        for card in to_remove:
            hand.remove(card)

    def play_action_cards(self, hand):
        pass

    def buy_card(self, money, card_name, condition=lambda: True):
        card_class = get_card_class(card_name)

        if money >= card_class.Cost and self.state.supply[card_class.Name()] > 0 and condition():
            ok = self.game_client.buy(card_name)
            return ok

        return False

    def buy(self, supply, money, buys):
        """This method should be implemented by derived classes

        """
        return False

    def buy_stuff(self, hand):
        while self.state.buys > 0:
            buys = self.state.buys
            supply = self.state.supply
            money = count_money(hand + self.state.play_area) - self.state.used_money

            if self.buy(supply, money, buys):
                continue

            for card_name, condition in (('Province', lambda: True),
                                         ('Gold', lambda: supply['Province'] >= 4),
                                         ('Duchy', lambda: supply['Province'] < 4),
                                         ('Silver', lambda: supply['Province'] >= 4 or supply['Duchy'] >= 4),
                                         ('Estate', lambda: supply['Province'] < 4 and supply['Duchy'] < 4)):
                if self.buy_card(money, card_name, condition):
                    break

            # Can't byt anything interesting
            break

    def play_card(self, card, hand):
        self.game_client.play_action_card(card.Name())
        hand.remove(card)

    def play(self):
        """
        """
        hand = self.state.hand
        self.play_no_brainers(hand)
        self.play_action_cards(hand)
        self.buy_stuff(hand)
        self.game_client.done()

    def respond(self, request, *args):
        return
