from abc import ABCMeta, abstractmethod


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
