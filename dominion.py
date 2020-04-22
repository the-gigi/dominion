import copy

from card_util import get_card_types
from cards import *
from computer_players.simpleton import Simpleton
from computer_players.rockefeller import Rockefeller
from computer_players.victor import Victor
from computer_players.the_guy import TheGuy
from game_factory import create_game_engine


def main():
    """ """
    card_types = get_card_types()[:10]
    players_info = dict(Vicky=Victor,
                        The_Rock=Rockefeller,
                        Guy=TheGuy)

    game_engine = create_game_engine(card_types, players_info)
    game_engine.run()


if __name__ == '__main__':
    main()
