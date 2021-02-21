import copy
import re

import time

from dominion_object_model import object_model
from dominion_game_engine import card_util, action_handlers
from dominion_game_engine.card_util import get_card_class


class Game(object_model.GameClient):
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

        self.waiting_for_response = False

    @property
    def player_states(self):
        return [p[1] for p in self.players]

    @property
    def player(self) -> object_model.Player:
        return self.players[self.active_player_index][0]

    @property
    def player_name(self) -> str:
        return self.players[self.active_player_index][1].name

    @property
    def other_players(self):
        return [p for i, p in enumerate(self.players) if i != self.active_player_index]

    def run(self, players, server=None):
        self.players = players

        turn = 0
        while not self.is_over:
            turn += 1
            print('***** turn ', turn, self.player_name)
            if server is not None and hasattr(server, 'Pump'):
                server.Pump()
                time.sleep(0.001)
            try:
                self.send_personal_state()
                self.current_player_done = False
                self.player.play()
                self.send_personal_state()
                while not self.current_player_done:
                    if server is not None and hasattr(server, 'Pump'):
                        server.Pump()
                    time.sleep(0.001)
                self.end_turn()
            except Exception as e:
                print(e)
                raise
            supply = self.piles
            print(f'cards: {self.player_state.all_cards}, total: {self.player_state.all_cards.count}')
            print(f'hand: {self.player_state.hand}')
            print(f'draw_deck: {self.player_state.draw_deck}')
            print(f'discard_pile: {self.player_state.discard_pile}')
            print(f'points: {self.count_player_points(self.player_state)}')
            print(
                f'supply - provinces: {supply["Province"]}, duchies: {supply["Duchy"]}, estates: {supply["Estate"]}, silver: {supply["Silver"]}')
            print('-' * 20)

            self.active_player_index = (self.active_player_index + 1) % len(self.players)
        self.handle_game_over()

    def handle_game_over(self):
        winners, scores = self.find_winners()
        if len(winners) == 1:
            message = f'{winners[0]} won the game!!!'
        else:
            message = f'The winners are {", ".join(winners[:-1])} and {winners[-1]}!!!'

        print('🎉 ' + message)
        victory_event = dict(
            event='game over',
            winners=winners,
            scores=scores
        )
        for p in self.players:
            p[0].on_game_event(victory_event)

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

    def _is_pile_empty(self, card_name):
        """Check if a card pile is empty

        return True if the pile of the given card type is empty and False otherwise
        """
        return self.piles[card_name] == 0

    def _verify_action(self, card_name):
        """verify that the player's card is an action, has the card in their hand, and has at least one action
        return True if the player can play the card, otherwise return False
        """
        card = get_card_class(card_name)
        is_action_card = card.Type == 'Action'
        is_card_in_hand = card.Name() in [card.Name() for card in self.player_state.hand]
        has_actions = self.player_state.actions > 0
        return is_action_card and is_card_in_hand and has_actions

    def _verify_buy(self, card_name):
        """verify the supply if not exhausted, player has enough money and has at least one buy"""
        card_class = get_card_class(card_name)
        if self.player_state.buys < 1:
            return False

        if self._is_pile_empty(card_name):
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
        scores = {}
        winners = []
        current_vp = 0
        current_coins = 0
        for player_state in self.player_states:
            vp = self.count_player_points(player_state)
            coins = self.count_player_money(player_state)
            scores[player_state.name] = (vp, coins)
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
        return winners, scores

    def send_game_event(self, event):
        for player, _ in self.players:
            player.on_game_event(event)

    def send_personal_state(self):
        for player, player_state in self.players:
            personal_state = player_state.get_personal_state(copy.deepcopy(self.piles))
            player.on_state_change(personal_state)

    def end_turn(self):
        """ """
        self.player_state.used_money = 0
        # artificial delay to prevent out of order state notifications
        time.sleep(0.1)
        self.send_personal_state()

    @property
    def is_over(self):
        """Check if all provinces are gone or 3 supply piles are empty

        return True if the game is over and False otherwise
        """
        if self.piles['Province'] == 0:
            return True
        empty_piles = 0
        # empty_piles = sum(1 if v == 0 else 0 for v in self.piles.values())
        for card_type, count in self.piles.items():
            if count == 0:
                empty_piles += 1
                if empty_piles >= 3:
                    return True
        return False

    def _respond(self, player, action, *args):
        """ """
        self.waiting_for_response = True
        response = player.respond(action, *args)
        self.waiting_for_response = False
        return response

    # GameClient interface
    def play_action_card(self, card_name):
        """
        Verify that the player can play the card
        Depending on the card, take its action
        Move the card from the player's hand to the play area
        """
        print(f'{self.player_name} played {card_name}')
        if self.waiting_for_response:
            print(f'Can\'t play {card_name}, waiting for response')
            return

        if not self._verify_action(card_name):
            print(f'Can\'t play {card_name}, could not verify action')
            return False

        ps = self.player_state
        # find the played card in the player's hand
        played_card = None
        for card in ps.hand:
            if card.Name() == card_name:
                played_card = card
                break

        if played_card is None:
            print(f'{self.player_name} tried to play a card {card_name} not in their hand')
            return False

        lower_card_name = re.sub(r'(?<!^)(?=[A-Z])', '_', card_name).lower()
        handler = getattr(action_handlers, 'play_' + lower_card_name)

        # move the card from the player's hand to the play area

        ps.hand.remove(played_card)
        ps.play_area.append(played_card)
        ps.actions -= 1

        self.send_personal_state()

        handler(self)

        self.send_game_event(f'{self.player_name} played {card_name}')
        self.send_personal_state()
        return True

    def buy(self, card_name):
        """ """
        if self.waiting_for_response:
            return

        if not self._verify_buy(card_name):
            return False

        card_class = get_card_class(card_name)

        self.piles[card_name] -= 1
        self.player_state.discard_pile.add_to_top([card_class()])
        self.player_state.buys -= 1
        self.send_game_event(f'{self.player_name} bought {card_name}')
        self.send_personal_state()

        return True

    def done(self):
        """ """
        if self.waiting_for_response:
            return
        self.player_state.done()
        self.current_player_done = True
