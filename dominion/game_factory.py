from collections import Mapping

from dominion.card_util import setup_piles
from dominion.game import Game
from dominion.game_client import GameClient
from dominion.object_model import BasePlayer
from dominion.player_state import PlayerState


def create_player(name, player_class: type(BasePlayer), game):
    game_client = GameClient(game)
    return player_class(name, game_client)


def start_game(card_types, players_info: Mapping):
    piles = setup_piles(card_types, len(players_info))

    player_states = {}
    players = []
    for name, player_class in players_info.items():
        player_state = PlayerState(name, piles)
        player_states[name] = (player_state)

    game = Game(piles)

    for name, player_class in players_info.items():
        try:
            player = create_player(name, player_class, game)
        except Exception as e:
            player = create_player(name, player_class, game)
        players.append((player, player_states[name]))

    game.run(players)
