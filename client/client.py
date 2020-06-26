from PodSixNet.Connection import connection, ConnectionListener

from dominion import object_model


class Client(ConnectionListener,
             object_model.GameClient,
             object_model.Player):
    def __init__(self, name, player: object_model.Player, host='127.0.0.1', port=5071):
        self.name = name
        self._player = player
        self._state = None
        self.Connect((host, port))

    def Loop(self):
        self.Pump()
        connection.Pump()

    # Player interface
    def play(self):
        pass

    def respond(self, action, *args):
        pass

    def on_game_event(self, event):
        pass

    # GameClient interface
    def play_action_card(self, card):
        self.Send(dict(action='play_action_card', card=card))

    def buy(self, card_type):
        self.Send(dict(action='buy', card_type=card_type))

    def done(self):
        self.Send(dict(action='done'))

    @property
    def state(self):
        return self._state

    # Server events
    def Network_on_player_join(self, data):
        print(f'*** player join: {data["player"]}')

    def Network_on_game_start(self, data):
        print('Game started!')

    def Network_on_state(self, data):
        self._state = data['state']

    # Server commands
    def Network_play(self, data):
        self.play()

    def Network_respond(self, data):
        self.respond(data['action_card'], data['args'])

    # built in stuff
    def Network_connected(self, data):
        print("You are now connected to the server")
        self.Send(dict(action='join', name=self.name))

    def Network_error(self, data):
        print('error:', data['error'][1])
        connection.Close()

    def Network_disconnected(self, data):
        print('Server disconnected')
        exit()


class DummyPlayer(object_model.Player):
    def play(self):
        pass

    def respond(self, action, *args):
        pass

    def on_game_event(self, event):
        pass


if __name__ == '__main__':
    cli = Client('dummy', DummyPlayer())
    while True:
        cli.Loop()
