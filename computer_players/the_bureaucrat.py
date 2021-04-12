from computer_players.base_computer_player import BaseComputerPlayer
from dominion_game_engine.hand import has_card_type, select_by_name


class TheBureaucrat(BaseComputerPlayer):
    def buy(self, supply, money, buys):
        return self.buy_card(money, 'Bureaucrat')

    def play_action_cards(self, hand):
        """ """
        if select_by_name(hand, ['Bureaucrat']):
            self.game_client.play_action_card('Bureaucrat')

    def respond(self, action, *args):
        if action != 'Cellar':
            return

        discard_cards = [c.Name() for c in self.state.hand if c.Type in ('Victory', 'Curse')]
        return discard_cards



