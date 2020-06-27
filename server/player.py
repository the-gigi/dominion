from dominion import object_model


class Player(object_model.Player):
    def __init__(self):
        """ """
        self._name = ''

    def play(self):
        pass

    def respond(self, action, *args):
        pass

    def on_game_event(self, event):
        pass

    def on_state_change(self, state):
        pass

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name
