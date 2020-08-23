from dominion_object_model import object_model
from dominion_grpc_client.client import Client


class DummyPlayer(object_model.Player):
    def __init__(self, game_client: object_model.GameClient):
        self.game_client = game_client

    def play(self):
        self.game_client.done()

    def respond(self, action, *args):
        return 'dummy'

    def on_game_event(self, event):
        print(event)

    def on_state_change(self, state):
        pass


if __name__ == '__main__':
    Client('dummy', DummyPlayer).run()
    #Client('dummy', DummyPlayer).run(host='35.202.145.215')
