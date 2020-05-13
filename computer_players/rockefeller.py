from computer_players.base_computer_player import BaseComputerPlayer
from dominion.player_state import *


class Rockefeller(BaseComputerPlayer):
    def buy(self, supply, money, buys):
        for card_type in (Gold, Silver, Copper):
            if self.buy_card(money, card_type):
                return True

        return False

    def respond(self, request, *args):
        return
