from collections import Mapping

from dominion.card_util import setup_piles
from dominion.game import Game
from dominion.game_client import GameClient
from dominion.player_state import PlayerState


def create_player(name, player_class, game, *args):
    game_client = GameClient(game)
    return player_class(name, game_client, *args)


def start_game(card_types, players_info: Mapping, server=None):
    piles = setup_piles(card_types, len(players_info))

    player_states = {}
    players = []
    for name, (player_class, _) in players_info.items():
        player_state = PlayerState(name, piles)
        player_states[name] = player_state

    game = Game(piles)
    if server is not None:
        server.attach_game_client(game)

    for name, (player_class, args) in players_info.items():
        args = () if args is None else args
        player = create_player(name, player_class, game, *args)
        players.append((player, player_states[name]))

    game.run(players, server)
