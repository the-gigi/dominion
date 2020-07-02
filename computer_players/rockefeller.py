from computer_players.base_computer_player import BaseComputerPlayer
from dominion.player_state import *


class Rockefeller(BaseComputerPlayer):
    def buy(self, supply, money, buys):
        for card_name in ('Gold', 'Silver', 'Copper'):
            if self.buy_card(money, card_name):
                return True

        return False

    def respond(self, request, *args):
        return
