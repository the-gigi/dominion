from computer_players.base_computer_player import BaseComputerPlayer
from dominion_game_engine.hand import select_by_name


class RobinHood(BaseComputerPlayer):
    def buy(self, supply, money, buys):
        return self.buy_card(money, 'Bandit')

    def play_action_cards(self, hand):
        """ """
        if select_by_name(hand, ['Bandit']):
            self.game_client.play_action_card('Bandit')
