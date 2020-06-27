import asyncio

from dominion.cards import *
from dominator.game_custom_resource import GameCustomResource
from dominator.player_custom_resource import PlayerCustomResource
from dominator.game_factory import create_game
from computer_players import (
    napoleon,
    rockefeller,
    the_guy,
    victor
)
from dominator.kube_client import kube_client

_lock = asyncio.Lock()


class Game:
    def __init__(self, name, num_players):
        self.game = GameCustomResource(name, kube_client)
        self.num_players = num_players
        self.players = {}
        self.computer_players = dict(
            Napoleon=napoleon.Napoleon,
            Rockefeller=rockefeller.Rockefeller,
            TheGuy=the_guy.TheGuy,
            Victor=victor.Victor
        )

    async def _async_join(self, name):
        async with _lock:
            if name in self.players:
                raise RuntimeError(f'Player {name} has already joined')

            if len(self.players) == self.num_players:
                raise RuntimeError(f'Game is full')

            player = PlayerCustomResource(name, kube_client)
            self.players[name] = player

            if len(self.players) == self.num_players:
                self._start()

    def join(self, name):
        asyncio.run(self._async_join(name))

    def get_computer_player(self, player_cr):
        return self.computer_players[player_cr.player_type]

    def _start(self):
        print(f'Starting game...')
        players_info = {name: self.get_computer_player(cr) for name, cr in self.players.items()}
        card_types = [
            Bureaucrat,
            Chancellor,
            CouncilRoom,
            Festival,
            Library,
            Militia,
            Moat,
            Spy,
            Thief,
            Village]

        dominion_game, players = create_game(card_types, players_info)

        for player, player_state in players:
            player_cr = player.game_client.player_cr
            personal_state = player_state.state
            try:
                player_cr.patch(body=dict(status=dict(state=personal_state)))
            except Exception as e:
                print(e)
                raise

        dominion_game.run(players)