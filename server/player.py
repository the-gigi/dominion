from dominion import object_model


class Player(object_model.Player):
    def __init__(self):
        """ """
        self._name = ''
        self._channel = None

    def play(self):
        self.channel.Send(dict(action='play'))

    def respond(self, action, *args):
        response = self.channel.Send(dict(action='play',args=args))
        return response

    def on_game_event(self, event):
        self.channel.Send(dict(action='on_game_event', event=event))

    def on_state_change(self, state):
        self.channel.Send(dict(action='on_state_change', state=state))

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def channel(self):
        return self._channel

    @channel.setter
    def channel(self, channel):
        self._channel = channel
