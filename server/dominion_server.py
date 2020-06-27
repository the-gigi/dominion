import random

from PodSixNet.Server import Server

from server import player_channel, config
from server.event_handler import EventHandler
from server.player import Player
from dominion import game_factory

MAX_PLAYER_COUNT = 2


class DominionServer(Server, EventHandler):
    def __init__(self):
        super().__init__(player_channel.PlayerChannel)
        self.players = {}

    def Connected(self, channel, addr):
        channel.attach_event_handler(self)
        player = Player
        self.players[addr] = player

    def start_game(self):
        """ """
        card_types = []
        players_info = {player.name: player for player in self.players.values()}
        computer_players = self.get_computer_players()
        for name, player in computer_players:
            players_info[name] = player

        game_factory.start_game(card_types, players_info)

    def get_computer_players(self):
        """ """
        joined_players = [p for p in self.players.values() if p.name]
        n = MAX_PLAYER_COUNT - len(joined_players)
        random.shuffle(config.computer_players)
        return config.computer_players[:n]

    # EventHandler interface implementation
    def on_start(self, channel):
        self.start_game()

    def on_join(self, channel, name):
        try:
            while name in (p.name for p in self.players.values()):
                name += str(random.randint(1, 10))
        except Exception as e:
            while name in (p.name for p in self.players.values()):
                name += str(random.randint(10))

        player = self.players[channel.addr]
        player.name = name

        if len(self.players) == MAX_PLAYER_COUNT:
            self.start_game()

    def on_play_action_card(self, channel, card):
        pass

    def on_buy(self, channel, card):
        pass

    def on_done(self, channel):
        pass

    def on_respond(self, channel, response):
        pass
