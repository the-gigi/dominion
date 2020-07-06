from computer_players.base_computer_player import BaseComputerPlayer
from dominion.card_util import get_card_class
from dominion.player_state import *
import random


class Napoleon(BaseComputerPlayer):
    def play_action_cards(self, hand):
        for i in range(self.state.actions):
            for card in hand:
                if isinstance(card, Militia):
                    self.play_card(card, hand)
                elif isinstance(card, Spy):
                    self.play_card(card, hand)

    def buy(self, supply, money, buys):
        if money == 4:
            number = random.randint(0, 2)
            card = 'Militia' if number == 1 else 'Spy'
            return self.buy_card(money, card)

        return False

    def play_card(self, card, hand):
        self.game_client.play_action_card(card.Name())
        hand.remove(card)

    def respond(self, request, *args):
        if request == 'Spy':
            top_card_names = args
            response = {}
            for name in top_card_names:
                card = get_card_class(name)
                response[name] = 'put_back'
                if name == self.name:
                    if card.Type in ('Victory', 'Curse'):
                        response[name] = 'discard'
                else:
                    if card.Type not in ('Victory', 'Curse'):
                        response[name] = 'discard'
            return response
