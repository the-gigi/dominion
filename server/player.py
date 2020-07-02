from dominion import object_model
from pprint import pprint as pp

class Player(object_model.Player):
    def __init__(self, name, game_client, channel):
        """ """
        self._name = name
        self._channel = channel

    def play(self):
        self.channel.Send(dict(action='play'))

    def respond(self, action, *args):
        response = self.channel.Send(dict(action='play',args=args))
        return response

    def on_game_event(self, event):
        self.channel.Send(dict(action='on_game_event', event=event))

    def on_state_change(self, state):
        state = state.as_dict()

        self.channel.Send(dict(action='on_state', state=state))

    @property
    def name(self):
        return self._name

    @property
    def channel(self):
        return self._channel

    def repr(self):
        return f'Player(name: {self.name}, addr: {self.channel.addr})'