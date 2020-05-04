from computer_players.base_computer_player import BaseComputerPlayer
from player_state import *
import random


class Napoleon(BaseComputerPlayer):
    def play_action_cards(self, hand):
        for i in range(self.personal_state.actions):
            for card in hand:
                if isinstance(card, Militia):
                    self.play_card(card, hand)
                elif isinstance(card, Spy):
                    self.play_card(card, hand)

    def buy(self, supply, money, buys):
        if money == 4:
            number = random.randint(0, 2)
            card = Militia if number == 1 else Spy
            return self.buy_card(money, card)

        return False

    def play_card(self, card, hand):
        self.game_client.play_action_card(card)
        hand.remove(card)

    def respond(self, request, *args):
        if request == Spy:
            top_cards = args[0]
            response = {}
            for name, top_card in top_cards.items():
                response[name] = 'put_back'
                if name == self.name:
                    if top_card.Type in ('Victory', 'Curse'):
                        response[name] = 'discard'
                else:
                    if top_card.Type not in ('Victory', 'Curse'):
                        response[name] = 'discard'
            return response
