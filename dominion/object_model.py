from abc import ABCMeta, abstractmethod

from dominion import card_util


class GameClient(metaclass=ABCMeta):
    @abstractmethod
    def play_action_card(self, card_type: str):
        pass

    @abstractmethod
    def buy(self, card_type: str):
        pass

    @abstractmethod
    def done(self):
        pass


class Game(metaclass=ABCMeta):
    @abstractmethod
    def find_winners(self):
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
    def respond(self, action, *args):
        """The player should return a proper response to the specific request

        this method may be called during the play of the active player
        while they play an action card on the active player and/or other
        players.

        Example:
            - in response to militia card all other players must discard to 3 cards
            - in response to an attack card, each player with  moat may block the attack
            - in response to a thief, the active player must select if/who to steal from
        """
        pass

    @abstractmethod
    def on_game_event(self, event):
        pass

    @abstractmethod
    def on_state_change(self, state):
        pass


class BasePlayer(Player):
    def __init__(self, name, game_client: GameClient, channel):
        self.name = name
        self.game_client = game_client
        self.events = []
        self._state = None

    @property
    def state(self):
        # return self.game_client.state
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