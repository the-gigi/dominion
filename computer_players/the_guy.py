from card_util import count_money
from object_model import BasePlayer
from cards import *
from player_state import *


class TheGuy(BasePlayer):
    def play(self):
        """
        Victor only buys the largest possible victory card
        """
        hand = self.personal_state.hand
        supply = self.personal_state.supply
        money = count_money(hand)
        play = self.game_client.play_action_card
        for card in hand:
            if isinstance(card, Village):
                play(Village)
            elif isinstance(card, Festival):
                play(Festival)
        for self.
            if CouncilRoom in hand:
                play(CouncilRoom)



        self.game_client.done()

        supply = self.personal_state.supply
        print(f'points: {self.personal_state.points}')
        print(f'supply - provinces: {supply[Province]}, duchies: {supply[Duchy]}, estates: {supply[Estate]},')
        print('-' * 20)

    def react(self, attack):
        return False
