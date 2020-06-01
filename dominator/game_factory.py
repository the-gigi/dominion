from collections import Mapping

from dominator.game_client import GameClient
from dominator.player_custom_resource import PlayerCustomResource

from dominion.game import Game as DominionGame
from dominion.card_util import setup_piles
from dominion.object_model import BasePlayer
from dominion.player_state import PlayerState
from dominator.kube_client import kube_client


def create_player(name: str, player_class: type(BasePlayer), player_cr: PlayerCustomResource):
    game_client = GameClient(player_cr)
    return player_class(name, game_client)


def create_game(card_types, players_info: Mapping):
    piles = setup_piles(card_types, len(players_info))

    player_states = {}
    players = []
    for name, player_class in players_info.items():
        player_state = PlayerState(name, piles)
        player_states[name] = (player_state)

    game = DominionGame(piles)

    for name, player_class in players_info.items():
        player = create_player(name, player_class, PlayerCustomResource(name, kube_client))
        player_state = player_states[name]
        players.append((player, player_state))

    return game, players
