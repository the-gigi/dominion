import inspect

import card_util
import object_model
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

    def count_player_points(self, player_state):
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

    def count_player_money(self, player_state):
        """Count the total amount of coins in
           the player's hand, deck and discard pile

           return the sum of all the coins
        """
        amount = 0
        all_cards = player_state.hand + player_state.draw_deck.cards + player_state.discard_pile.cards
        return card_util.count_money(all_cards)

    def is_pile_empty(self, card_type):
        """Check if a card pile is empty

        return True if the pile of the given card type is empty and False otherwise
        """
        return self.piles[card_type] == 0

    def verify_action(self, card):
        """verify that the player's card is an action, has the card in their hand, and has at least one action
        return True if the player can play the card, otherwise return False
        """
        is_action_card = card.Type == 'Action'
        is_card_in_hand = card in self.player_state.hand
        has_actions = self.player_state.actions > 0
        return is_action_card and is_card_in_hand and has_actions

    def verify_buy(self, card_type):
        """verify the player has enough money and has at least one buy"""
        amount = card_util.count_money(self.player_state.hand)
        if amount < card_type.Cost:
            return False
        return self.player_state.buys > 0

    # Game interface
    def find_winner(self):
        """The winner is the player with the most victory points

        In case of a tie the money is the tie breaker

        Returns the winning player
        """
        raise NotImplementedError

    def end_turn(self):
        """

        :return:
        """

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

    def buy(self, card):
        """ """
        raise NotImplementedError

    def done(self):
        """ """
        self.player_state.done()

    @property
    def state(self):
        raise NotImplementedError
