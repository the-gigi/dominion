import json
import time

from dominion_object_model import object_model
from dominion_grpc_proto.dominion_pb2 import Message


class Player(object_model.Player):
    response = None

    def __init__(self, main_queue, response_queue, name, *args):
        """ """
        self._name = name
        self._main_queue = main_queue
        self._response_queue = response_queue

    def play(self):
        self._main_queue.put(Message(type='play'))

    def _adapt_response(self, response):
        if response.payload is None:
            return

        action = response.card.name
        payload = json.loads(response.payload)
        # if action in ('Militia', 'Cellar', 'Harbinger'):
        #     return payload
        return payload

    def respond(self, action, *args):
        data = json.dumps(dict(action=action, args=args))
        self._response_queue.put(Message(type='respond', data=data))
        # wait for response
        while Player.response is None:
            time.sleep(0.1)
        response = self._adapt_response(Player.response)
        Player.response = None
        return response

    def on_game_event(self, event):
        self._main_queue.put(Message(type='on_game_event', data=json.dumps(event)))

    def on_state_change(self, state):
        state = json.dumps(state.as_dict())
        self._main_queue.put(Message(type='on_state_change', data=state))

    @property
    def name(self):
        return self._name

    def repr(self):
        return f'Player(name: {self.name})'

    def on_response(self, response):
        self._response = response
