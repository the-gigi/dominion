from PodSixNet.Server import Server

from server import player_channel
from server.event_handler import EventHandler
from server.player import Player


class DominionServer(Server, EventHandler):
    def __init__(self):
        super().__init__(player_channel.PlayerChannel)
        self.players = {}

    def Connected(self, channel, addr):
        channel.attach_event_handler(self)
        player = Player()
        self.players[addr] = player

    def on_start(self, channel):
        pass

    def on_join(self, channel, name):
        pass

    def on_play_action_card(self, channel, card):
        pass

    def on_buy(self, channel, card):
        pass

    def on_done(self, channel):
        pass

    def on_respond(self, channel, response):
        pass


