from computer_players.base_computer_player import BaseComputerPlayer
from player_state import *


class Napoleon(BaseComputerPlayer):
    def play_action_cards(self, hand):
        for i in range(self.personal_state.actions):
            for card in hand:
                if isinstance(card, Militia):
                    self.play_card(card, hand)

    def buy(self, supply, money, buys):
        if money == 4:
            return self.buy_card(money, Militia)

        return False

    def play_card(self, card, hand):
        self.game_client.play_action_card(card)
        hand.remove(card)

    def respond(self, request, *args):
        return

