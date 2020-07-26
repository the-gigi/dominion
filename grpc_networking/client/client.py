from dominion_object_model import object_model
from dominion_grpc_client.client import Client


class DummyPlayer(object_model.Player):
    def __init__(self, game_client):
        self.game_client = game_client

    def play(self):
        self.game_client.done()

    def respond(self, action, *args):
        pass

    def on_game_event(self, event):
        pass

    def on_state_change(self, state):
        pass


if __name__ == '__main__':
    Client('dummy', DummyPlayer).run()
