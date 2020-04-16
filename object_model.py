from abc import ABCMeta, abstractmethod

import card_util


class GameClient(metaclass=ABCMeta):
    @abstractmethod
    def play_action_card(self, card):
        pass

    @abstractmethod
    def buy(self, card_type):
        pass

    @abstractmethod
    def done(self):
        pass

    # @property
    # @abstractmethod
    # def state(self):
    #     pass


class Game(metaclass=ABCMeta):
    @abstractmethod
    def find_winners(self):
        pass

    @abstractmethod
    def start_turn(self):
        pass

    @abstractmethod
    def end_turn(self):
        pass

    @property
    @abstractmethod
    def is_over(self):
        pass


class Player(metaclass=ABCMeta):
    @abstractmethod
    def play(self):
        pass

    @abstractmethod
    def react(self, attack):
        """The player should return True if it wants to block the attack and False otherwise"""
        pass

    @abstractmethod
    def on_event(self, event):
        pass


class BasePlayer(Player):
    def __init__(self, name, game_client: GameClient):
        self.name = name
        self.game_client = game_client
        self.events = []

    @property
    def personal_state(self):
        return self.game_client.personal_state

    @property
    def all_cards(self):
        hand = card_util.as_dict(self.personal_state.hand)
        draw_deck = card_util.as_dict(self.personal_state.draw_deck.cards)
        return dict(**hand, **draw_deck, **self.personal_state.discard_pile)

    def on_event(self, event):
        self.events.append(event)
