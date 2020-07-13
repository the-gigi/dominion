from dominion import card_util
from dominion.card_util import count_money, get_card_class
from dominion.cards import *
from dominion.object_model.object_model import Player, GameClient


class BaseComputerPlayer(Player):
    def __init__(self, name, game_client: GameClient):
        self.name = name
        self.game_client = game_client
        self.events = []
        self._state = None

    def play_no_brainers(self, hand):
        play = self.game_client.play_action_card
        to_remove = []
        for card in hand:
            if isinstance(card, Village):
                play(card.Name())
                to_remove.append(card)
            elif isinstance(card, Festival):
                play(card.Name())
                to_remove.append(card)
            elif isinstance(card, Market):
                play(card.Name())
                to_remove.append(card)

        for card in to_remove:
            hand.remove(card)

    def play_action_cards(self, hand):
        pass

    def buy_card(self, money, card_name, condition=lambda: True):
        card_class = get_card_class(card_name)

        if money >= card_class.Cost and self.state.supply[card_name] > 0 and condition():
            ok = self.game_client.buy(card_name)
            return ok

        return False

    def buy(self, supply, money, buys):
        """This method should be implemented by derived classes

        """
        return False

    def buy_stuff(self, hand):
        while self.state.buys > 0:
            buys = self.state.buys
            supply = self.state.supply
            money = count_money(hand + self.state.play_area) - self.state.used_money

            if self.buy(supply, money, buys):
                continue

            for card_name, condition in (('Province', lambda: True),
                                         ('Gold', lambda: supply['Province'] >= 4),
                                         ('Duchy', lambda: supply['Province'] < 4),
                                         ('Silver', lambda: supply['Province'] >= 4 or supply['Duchy'] >= 4),
                                         ('Estate', lambda: supply['Province'] < 4 and supply['Duchy'] < 4)):
                if self.buy_card(money, card_name, condition):
                    break

            # Can't byt anything interesting
            break

    def play_card(self, card, hand):
        self.game_client.play_action_card(card.Name())
        print('###### played ', card.Name())
        hand.remove(card)

    def play(self):
        """
        """
        hand = self.state.hand
        print(f'@@@@ play(), name: {self.name}, hand: {hand}')
        self.play_no_brainers(hand)
        self.play_action_cards(hand)
        self.buy_stuff(hand)
        self.game_client.done()

    @property
    def state(self):
        return self._state

    @property
    def all_cards(self):
        hand = card_util.as_dict(self.state.hand)
        draw_deck = card_util.as_dict(self.state.draw_deck.cards)
        return dict(**hand, **draw_deck, **self.state.discard_pile)

    def on_game_event(self, event):
        self.events.append(event)

    def on_state_change(self, state):
        self._state = state

    def respond(self, action, *args):
        return
