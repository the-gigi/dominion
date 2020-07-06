import random

from PodSixNet.Server import Server

from server import player_channel, config
from server.event_handler import EventHandler
from server.player import Player
from dominion import game_factory

MAX_PLAYER_COUNT = 4


class DominionServer(Server, EventHandler):
    def __init__(self):
        super().__init__(player_channel.PlayerChannel)
        self.game_client = None
        self.players = {}

    def attach_game_client(self, game_client):
        self.game_client = game_client

    def Connected(self, channel, addr):
        channel.attach_event_handler(self)
        self.players[addr] = ('', Player, channel)

    def start_game(self):
        """ """
        # Remove unjoined players
        self.players = {k: v for k, v in self.players.items() if v[0] != ''}
        players_info = {p[1][0]: (p[1][1], p[1][2]) for p in self.players.items()}
        computer_players = self.get_computer_players()
        for name, player in computer_players:
            players_info[name] = (player, None)

        # Send 'game start' event to all players with cards and player names
        player_names = [p[0] for p in self.players.values()] + [name for name, _ in computer_players]
        card_names = [c.Name() for c in config.card_types]
        for p in self.players.values():
            p[2].Send(dict(action='on_game_start',
                           card_names=card_names,
                           player_names=player_names))

        game_factory.start_game(config.card_types, players_info, self)

    def get_computer_players(self):
        """ """
        joined_players = [p for p in self.players.values() if p[0]]
        n = MAX_PLAYER_COUNT - len(joined_players)
        random.shuffle(config.computer_players)
        return config.computer_players[:n]

    # EventHandler interface implementation
    def on_start(self, channel):
        self.start_game()

    def on_join(self, channel, name):
        if name == '':
            raise RuntimeError('Player name must not be empty')

        while name in (p[0] for p in self.players.values()):
            name += str(random.randint(1, 10))

        joined_players = [p for p in self.players.values() if p[0] != '']
        for p in joined_players:
            p[2].Send(dict(action='on_player_join', name=name))

        new_player = (name, Player, channel)
        self.players[channel.addr] = new_player

        if len(joined_players) == MAX_PLAYER_COUNT - 1:
            self.start_game()

    def on_play_action_card(self, channel, card):
        self.game_client.play_action_card(card)

    def on_buy(self, channel, card):
        self.game_client.buy(card)

    def on_done(self, channel):
        self.game_client.done()

    def on_respond(self, channel, response):
        pass
