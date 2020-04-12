import inspect

import card_util
import object_model
from card_stack import CardStack
from cards import *
import cards


class Game(object_model.Game,
           object_model.GameClient):
    """Game represents the specific game domain

    In this case Dominion
    """

    def __init__(self, piles, player_states):
        # The state of the game
        self.piles = piles
        self.player_states = player_states

        # The active player
        self.active_player_index = 0

    @property
    def player_state(self):
        return self.player_states[self.active_player]

    @property
    def personal_player_state(self):
        return self.player_state.personal_state

    @property
    def active_player(self):
        return self.active_player_index

    @active_player.setter
    def active_player(self, player_index):
        self.active_player_index = player_index

    @staticmethod
    def count_player_points(player_state):
        """Count the total victory points in
           the player's hand, deck and discard pile

           return the number of victory points
        """
        vp = 0
        all_cards = player_state.hand + player_state.draw_deck.cards + player_state.discard_pile.cards
        for card in all_cards:
            if isinstance(card, Province):
                vp += 6
            elif isinstance(card, Duchy):
                vp += 3
            elif isinstance(card, Estate):
                vp += 1
            elif isinstance(card, Curse):
                vp -= 1
        return vp

    @staticmethod
    def count_player_money(player_state):
        """Count the total amount of coins in
           the player's hand, deck and discard pile

           return the sum of all the coins
        """
        all_cards = player_state.hand + player_state.draw_deck.cards + player_state.discard_pile.cards
        return card_util.count_money(all_cards)

    def _is_pile_empty(self, card_type):
        """Check if a card pile is empty

        return True if the pile of the given card type is empty and False otherwise
        """
        return self.piles[card_type] == 0

    def _verify_action(self, card):
        """verify that the player's card is an action, has the card in their hand, and has at least one action
        return True if the player can play the card, otherwise return False
        """
        is_action_card = card.Type == 'Action'
        is_card_in_hand = card in self.player_state.hand
        has_actions = self.player_state.actions > 0
        return is_action_card and is_card_in_hand and has_actions

    def _verify_buy(self, card_type):
        """verify the supply if not exhausted, player has enough money and has at least one buy"""
        if self._is_pile_empty(card_type):
            return False

        amount = card_util.count_money(self.player_state.hand)
        if amount < card_type.Cost:
            return False
        return self.player_state.buys > 0

    # Game interface
    def find_winners(self):
        """The winner is the player with the most victory points

        In case of a tie the money is the tie breaker

        Returns a list with the winning player(s)

        In case of a money tie everyone is a winner and it returns a list of all names
        """
        winners = []
        current_vp = 0
        for player_state in self.player_states:
            vp = self.count_player_points(player_state)
            if winners == []:
                winners = [player_state.name]
                current_vp = vp
            elif vp > current_vp:
                winners = [player_state.name]
                current_vp = vp
            elif vp == current_vp:
                winners += [player_state.name]
        return winners

    def end_turn(self):
        """

        :return:
        """
        self.player_state.sync_personal_state()

    @property
    def is_over(self):
        """Check if all provinces are gone or 3 supply piles are empty

        return True if the game is over and False otherwise
        """
        if self.piles[cards.Province] == 0:
            return True
        empty_piles = 0
        # empty_piles = sum(1 if v == 0 else 0 for v in self.piles.values())
        for card_type in self.piles.keys():
            if self.piles[card_type] == 0:
                empty_piles += 1
                if empty_piles >= 3:
                    return True
        return False

    # GameClient interface
    def play_action_card(self, card):
        """ """
        raise NotImplementedError


    def buy(self, card_type):
        """ """
        if not self._verify_buy(card_type):
            return False

        self.piles[card_type] -= 1
        self.player_state.discard_pile.add_to_top([card_type()])
        self.player_state.sync_personal_state()

    def done(self):
        """ """
        self.player_state.done()