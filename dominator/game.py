from kubernetes import client, config

from dominator.game_custom_resource import GameCustomResource
from dominator.player_custom_resource import PlayerCustomResource

from computer_players import (
    napoleon,
    rockefeller,
    the_guy,
    victor
)


class Game:
    def __init__(self, name, num_players):
        config.load_kube_config()
        self.kube_client = client.CustomObjectsApi()
        self.game = GameCustomResource(name, self.kube_client)
        self.num_players = num_players
        self.players = {}
        self.computer_players = dict(
            Napoleon=napoleon.Napoleon,
            Rockefeller = rockefeller.Rockefeller,
            TheGuy = the_guy.TheGuy,
            Victor = victor.Victor
        )

    def join(self, name):
        if name in self.players:
            raise RuntimeError(f'Player {name} has already joined')

        if len(self.players) == self.num_players:
            raise RuntimeError(f'Game is full')

        player = PlayerCustomResource(name, self.kube_client)
        self.players[name] = player

    def get_computer_player(self, player_cr):
        return self.computer_players[player_cr.spec.playerType]

    def _start(self):
        players_info = {name: self.get_computer_player(cr) for name, cr in self.players.items()}


