from cards import *
from player_state import PlayerState




class GameState:
    def __init__(self, piles, player_states):
        """ """
        self.piles = piles
        self.player_states = [PlayerState(name) for name in player_names]

        num_players = len(player_names)
        self.piles = {c: 13 for c in card_types}

        self.piles[Copper] = copper_count - num_players * 7
        self.piles[Silver] = silver_count
        self.piles[Gold] = gold_count

        self.piles[Estate] = 8 if num_players == 2 else 12
        self.piles[Duchy] = 8 if num_players == 2 else 12
        self.piles[Province] = 8 if num_players == 2 else 12
        self.piles[Curse] = (num_players - 1) * 10
