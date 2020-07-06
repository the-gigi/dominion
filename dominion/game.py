import copy
import re
import time

from dominion import card_util, cards, object_model
from dominion.card_util import get_card_class
from dominion.cards import *


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
        self.current_player_done = False

    @property
    def player_states(self):
        return [p[1] for p in self.players]

    @property
    def player(self) -> object_model.Player:
        return self.players[self.active_player_index][0]

    @property
    def other_players(self):
        return [p for i, p in enumerate(self.players) if i != self.active_player_index]

    def run(self, players, server=None):
        self.players = players

        while not self.is_over:
            if server is not None:
                server.Pump()
                time.sleep(0.001)
            try:
                self.notify_player()
                self.current_player_done = False
                self.player.play()
                while server is not None and not self.current_player_done:
                    server.Pump()
                    time.sleep(0.001)
                self.end_turn()
            except Exception as e:
                print(e)
                raise
            supply = self.piles
            points = self.count_player_points(self.player_state)
            print(f'points: {points}')
            print(
                f'supply - provinces: {supply["Province"]}, duchies: {supply["Duchy"]}, estates: {supply["Estate"]}, silver: {supply["Silver"]}')
            print('-' * 20)

            self.active_player_index = (self.active_player_index + 1) % len(self.players)

        winners = self.find_winners()
        if len(winners) == 1:
            message = f'🎉 {winners[0]} won the game!!!'
        else:
            message = f'🎉 The winners are {", ".join(winners[:-1])} and {winners[-1]}!!!'
        print(message)

        for p in self.players:
            p.on_game_event(message)
        server.Pump()

    @property
    def player_state(self):
        return self.players[self.active_player_index][1]

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

    def _verify_action(self, card_name):
        """verify that the player's card is an action, has the card in their hand, and has at least one action
        return True if the player can play the card, otherwise return False
        """
        card = get_card_class(card_name)
        is_action_card = card.Type == 'Action'
        is_card_in_hand = card.Name() in [card.Name() for card in self.player_state.hand]
        has_actions = self.player_state.actions > 0
        return is_action_card and is_card_in_hand and has_actions

    def _verify_buy(self, card_type):
        """verify the supply if not exhausted, player has enough money and has at least one buy"""
        card_class = get_card_class(card_type)
        if self.player_state.buys < 1:
            return False

        if self._is_pile_empty(card_type):
            return False
        cm = card_util.count_money
        amount = cm(self.player_state.hand) + cm(self.player_state.play_area, False) - self.player_state.used_money
        if amount < card_class.Cost:
            return False

        self.player_state.used_money += card_class.Cost
        return True

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
        for player_state in self.player_states:
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

    def notify_player(self):
        personal_state = self.player_state.get_personal_state(copy.deepcopy(self.piles))
        self.player.on_state_change(personal_state)

    def end_turn(self):
        """ """
        self.player_state.used_money = 0
        self.notify_player()

    @property
    def is_over(self):
        """Check if all provinces are gone or 3 supply piles are empty

        return True if the game is over and False otherwise
        """
        if self.piles[cards.Province.Name()] == 0:
            return True
        empty_piles = 0
        # empty_piles = sum(1 if v == 0 else 0 for v in self.piles.values())
        for card_type, count in self.piles.items():
            if count == 0:
                empty_piles += 1
                if empty_piles >= 3:
                    return True
        return False

    # GameClient interface
    def play_action_card(self, card_name):
        """
        Verify that the player can play the card
        Depending on the card, take its action
        Move the card from the player's hand to the play area
        """
        if not self._verify_action(card_name):
            return False

        lower_card_name = re.sub(r'(?<!^)(?=[A-Z])', '_', card_name).lower()
        handler = getattr(self, 'play_' + lower_card_name)
        handler()

        # find the played card in the player's hand
        played_card = None
        for card in self.player_state.hand:
            if card.Name() == card_name:
                played_card = card
                break

        # move the card from the player's hand to the play area
        self.player_state.hand.remove(played_card)
        self.player_state.play_area.append(played_card)

        self.player_state.actions -= 1
        self.notify_player()
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
        self.player_state.draw_cards(1)
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

        def choose_hand():
            """The expected response is a set of 3 cards from the player's hand

            If the response is different return None
            """
            if isinstance(response, Moat):
                if response in player_state.hand:
                    return None

            if not isinstance(response, set) or len(response) != 3:
                return player_state.hand[:3]

            for card in response:
                if card not in player_state.hand:
                    return player_state.hand[:3]

            return response

        for player, player_state in self.other_players:
            response = player.respond(Militia)
            hand = choose_hand()
            if hand is None:
                break
            discarded = [c for c in player_state.hand if c not in hand]

            player_state.hand = hand
            player_state.discard_pile.add_to_top(discarded)
            self.notify_player()

    def play_bureaucrat(self):
        """
            Gain a silver card; put it on top of your deck.
            Each other player reveals a Victory card from
            his hand and puts it on top of his deck (or reveals
            a hand with no Victory cards).
        """

        def choose_victory(response):
            is_victory = response.Type == "Victory"
            in_hand = response in player_state.hand
            victory = response if is_victory and in_hand else None
            return victory

        if self._is_pile_empty(Silver):
            self.piles[Silver] -= 1
            self.player_state.draw_deck.add_to_top([Silver()])
        for player, player_state in self.other_players:
            response = player.respond(Bureaucrat)
            victory = choose_victory(response)
            if victory is not None:
                player_state.draw_deck.add_to_top([victory])
                player_state.hand.remove(victory)
            rest = (p for p in self.other_players + self.player if p != player)
            event = victory if victory else player_state.hand
            for p in rest:
                p.on_game_event(event)

    def play_spy(self):
        """+1 Card
        +1 Action

        Each player (including you) reveals the top card of his deck
        and either discards it or puts it back, your choice.
        """

        self.player_state.draw_cards(1)
        self.player_state.actions += 1

        top_cards = {}
        for player_state in self.player_states:
            player_state.reload_deck(1)
            top_card = player_state.draw_deck.cards[0]
            top_cards[player_state.name] = top_card
        response = self.player.respond(Spy, top_cards)
        for player_state in self.player_states:
            if response[player_state.name] == 'discard':
                card = player_state.draw_deck.pop(1)
                player_state.discard_pile.cards += card

    def play_thief(self):
        """ Each other player reveals the top 2 cards of his deck.
        If they revealed any Treasure cards, they trash one of them that you choose.
        You may gain any or all of these trashed cards.
        They discard the other revealed cards.
        """
        treasure_dict = {}
        for name, player_state in self.other_players:
            top_2 = player_state.draw_deck.peek(2)
            treasures = [c for c in top_2 if c.Type == 'Treasure']
            treasure_dict[name] = treasures
        response = self.player.respond(Thief, treasure_dict)
        for name, player_state in self.other_players:
            index, action = response[name]
            top_2 = player_state.draw_deck.pop(2)
            discard = player_state.discard_pile.add_to_top
            gain = self.player_state.discard_pile.add_to_top
            if index == 0:
                discard(top_2[1])
                if action == 'gain':
                    gain(top_2[0])
            elif index == 1:
                discard(top_2[0])
                if action == 'gain':
                    gain(top_2[1])
            else:
                discard(top_2[0])
                discard(top_2[1])

    def buy(self, card_name):
        """ """
        if not self._verify_buy(card_name):
            return False

        card_class = get_card_class(card_name)

        self.piles[card_name] -= 1
        self.player_state.discard_pile.add_to_top([card_class()])
        self.player_state.buys -= 1
        self.notify_player()

    def done(self):
        """ """
        self.current_player_done = True
        self.player_state.done()
