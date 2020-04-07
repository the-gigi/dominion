from collections import Mapping

from card_stack import CardStack
from cards import *
from game import Game
from game_client import GameClient
from game_engine import GameEngine
from object_model import BasePlayer
from personal_state import PersonalState
from player_state import PlayerState

copper_count = 60
silver_count = 40
gold_count = 30


def create_player(name, player_class: type(BasePlayer), player_state, game):
    personal_state = PersonalState(player_state.hand[:], CardStack())
    game_client = GameClient(personal_state, game)
    return player_class(name, game_client)


def create_game_engine(card_types, players_info: Mapping):
    num_players = len(players_info)
    piles = {c: 13 for c in card_types}

    piles[Copper] = copper_count - num_players * 7
    piles[Silver] = silver_count
    piles[Gold] = gold_count

    piles[Estate] = 8 if num_players == 2 else 12
    piles[Duchy] = 8 if num_players == 2 else 12
    piles[Province] = 8 if num_players == 2 else 12
    piles[Curse] = (num_players - 1) * 10

    player_states = {}
    players = []
    for name, player_class in players_info.items():
        player_state = PlayerState(name)
        player_states[name] = player_state

    game = Game(piles, list(player_states.values()))

    for name, player_class in players_info.items():
        player_state = player_states[name]
        players.append(create_player(name, player_class, player_state, game))

    game_engine = GameEngine(game, players)

    return game_engine
