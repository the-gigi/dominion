from PodSixNet.Connection import connection, ConnectionListener
from dominion.object_model import object_model


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
        self._player.play()
        self.done()

    def respond(self, action, *args):
        self._player.respond(action, *args)

    def on_game_event(self, event):
        self._player.on_game_event(event)

    def on_state_change(self, state):
        self._player.on_state_change(state)

    # GameClient interface
    def play_action_card(self, card_type):
        self.Send(dict(action='play_action_card', card=card_type))

    def buy(self, card_type):
        self.Send(dict(action='buy', card_type=card_type))

    def done(self):
        self.Send(dict(action='done'))

    @property
    def state(self):
        return self._state

    def Network(self, data):
        print(data)

    # Server events
    def Network_on_player_join(self, data):
        message = f'Player joined: {data["name"]}'
        print(message)
        self.on_game_event(message)

    def Network_on_game_start(self, data):
        message = 'Game started!'
        print(message)
        card_names = data['card_names']
        player_names = data['player_names']
        self.on_game_event(message)

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

    def on_state_change(self, state):
        pass


if __name__ == '__main__':
    cli = Client('dummy', DummyPlayer())
    while True:
        cli.Loop()
