import json

from dominion.object_model import object_model
from grpc_networking.proto.dominion_pb2 import Message


class Player(object_model.Player):
    def __init__(self, name, game_client, queue=None):
        """ """
        self._name = name
        self._queue = queue

    def play(self):
        self._queue.put(Message(type='play'))

    def respond(self, action, *args):
        data = json.dumps(dict(action=action, args=args))
        self._queue.put(Message(type='respond', data=data))

    def on_game_event(self, event):
        self._queue.put(Message(type='on_game_event', data=json.dumps(event)))

    def on_state_change(self, state):
        state = json.dumps(state.as_dict())
        self._queue.put(Message(type='on_state_change', data=state))

    @property
    def name(self):
        return self._name

    def repr(self):
        return f'Player(name: {self.name})'
