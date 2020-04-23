import copy
import re

import card_util
import object_model
from cards import *
import cards


class Game(object_model.Game,
           object_model.GameClient):
    """Game represents the specific game domain

    In this case Dominion
    """

    def __init__(self, piles):
        # The state of the game
        self.piles = piles

        # The active player
        self.active_player_index = 0

        self.players = []

    @property
    def player_states(self):
        return [p[1] for p in self.players]

    @property
    def player(self):
        return self.players[self.active_player_index][0]

    @property
    def other_players(self):
        return [p for i, p in enumerate(self.players) if i != self.active_player_index]

    def run(self, players):
        self.players = players

        while not self.is_over:
            self.player.play()
            self.end_turn()
            self.active_player_index = (self.active_player_index + 1) % len(self.players)

        winners = self.find_winners()
        if len(winners) == 1:
            print(f'🎉 {winners[0]} won the game!!!')
        else:
            print(f'🎉 The winners are {", ".join(winners[:-1])} and {winners[-1]}!!!')

    @property
    def player_state(self):
        return self.players[self.active_player_index][1]

    @property
    def personal_player_state(self):
        return self.player_state.personal_state

    def set_active_player_index(self, player_index):
        self.active_player_index = player_index

    @staticmethod
    def count_player_points(player_state):
        """Count the total amount of coins in
           the player's hand, deck and discard pile

           return the sum of all the coins
        """
        all_cards = player_state.hand + player_state.draw_deck.cards + player_state.discard_pile.cards
        return card_util.count_points(all_cards)

    @staticmethod
    def count_player_money(player_state):
        """
        Count the total amount of coins in
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
        cm = card_util.count_money
        amount = cm(self.player_state.hand) + cm(self.player_state.play_area, False)
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
        current_coins = 0
        for _, player_state in self.players:
            vp = self.count_player_points(player_state)
            coins = self.count_player_money(player_state)
            if not winners:
                winners = [player_state.name]
                current_vp = vp
                current_coins = coins
            elif vp > current_vp:
                winners = [player_state.name]
                current_vp = vp
                current_coins = coins
            elif vp == current_vp:
                if coins > current_coins:
                    winners = [player_state.name]
                    current_coins = coins
                elif coins == current_coins:
                    winners += [player_state.name]
        return winners

    def start_turn(self):
        """ """
        self.player_state.sync_personal_state(copy.deepcopy(self.piles))

    def end_turn(self):
        """ """
        self.player_state.sync_personal_state(copy.deepcopy(self.piles))

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
        """
        Verify that the player can play the card
        Depending on the card, take its action
        Move the card from the player's hand to the play area
        """
        if not self._verify_action(card):
            return False

        card_type = re.sub(r'(?<!^)(?=[A-Z])', '_', card.Name).lower()
        handler = getattr(self, 'play_' + card_type)
        handler()

        # # take action based on card type
        # if type(card) == Moat:
        #     self.play_moat()
        # elif type(card) == Chancellor:
        #     self.play_chancellor()
        # elif type(card) == Festival:
        #     self.play_festival()
        # elif type(card) == Village:
        #     self.play_village()
        # elif type(card) == CouncilRoom:
        #     self.play_council_room()

        # move the card from the player's hand to the play area
        self.player_state.hand.remove(card)
        self.player_state.play_area.append(card)

        self.player_state.actions -= 1
        self.player_state.sync_personal_state(copy.deepcopy(self.piles))
        return True

    def play_moat(self):
        """
        The active player draws 2 cards and adds them to their hand.

        Counter - When another player plays an Attack card, you may first
        reveal this from your hand, to be unaffected by it.
        """
        self.player_state.draw_cards(2)

    def play_chancellor(self):
        """
        +$2

        You may immediately put your deck into your discard pile.
        """
        # TO DO - Ask player if they want to put their deck into their discard pile

    def play_festival(self):
        """
        +2 Actions
        +1 Buy
        +$2
        """
        self.player_state.actions += 2
        self.player_state.buys += 1

    def play_village(self):
        """
        +1 Card
        +2 Actions
        """
        self.player_state.hand += self.player_state.draw_deck.cards[0]
        self.player_state.actions += 2

    def play_council_room(self):
        """
        +4 Cards
        +1 Buy

        Each other player draws a card.
        """
        self.player_state.draw_cards(3)
        self.player_state.buys += 1
        for player_state in self.player_states:
            player_state.draw_cards(1)

    def play_militia(self):
        """
        +$2

        Each player discards down to 3 cards in his hand.
        """

        def validate_response(cards):
            """The expected response is a set of 3 cards from the player's hand

            If the response is different return None
            """
            if not isinstance(cards, set) or len(cards) != 3:
                return None

            for card in cards:
                if not card in player.hand:
                    return None

            return cards

        for player, player_state in self.other_players:
            response = player.respond(Militia)
            cards = validate_response(response)
            if cards is None:
                discarded = player_state.hand[3:]
                new_hand = player_state.hand[:3]
            else:
                new_hand = cards
                discarded = [c for c in player.hand if c not in new_hand]

            player_state.hand = new_hand
            player_state.discard_pile.add_to_top(discarded)

    def buy(self, card_type):
        """ """
        if not self._verify_buy(card_type):
            return False

        self.piles[card_type] -= 1
        self.player_state.discard_pile.add_to_top([card_type()])
        self.player_state.sync_personal_state(copy.deepcopy(self.piles))

    def done(self):
        """ """
        self.player_state.done()
