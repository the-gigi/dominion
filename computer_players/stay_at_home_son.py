from computer_players.base_computer_player import BaseComputerPlayer
from dominion_game_engine.hand import has_card_type, select_by_name


class StayAtHomeSon(BaseComputerPlayer):
    def buy(self, supply, money, buys):
        return self.buy_card(money, 'Cellar')

    def play_action_cards(self, hand):
        """ """
        if select_by_name(hand, ['Cellar']):
            self.game_client.play_action_card('Cellar')

    def respond(self, action, *args):
        if action != 'Cellar':
            return

        discard_cards = [c.Name() for c in self.state.hand if c.Type in ('Victory', 'Curse')]
        return discard_cards



