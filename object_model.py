from abc import ABCMeta, abstractmethod


class GameClient(metaclass=ABCMeta):
    @abstractmethod
    def play_action_card(self, card):
        pass

    @abstractmethod
    def buy(self, card):
        pass

    @abstractmethod
    def done(self):
        pass

    @property
    @abstractmethod
    def state(self):
        pass


class Game(metaclass=ABCMeta):
    @abstractmethod
    def find_winner(self):
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

    def on_event(self, event):
        self.events.append(event)
