import copy

from card_util import get_card_types
from computer_players.simpleton import Simpleton
from computer_players.rockefeller import Rockefeller
from computer_players.victor import Victor
from computer_players.the_guy import TheGuy
from computer_players.napoleon import Napoleon
from game_factory import start_game
from cards import Militia


def main():
    """ """
    card_types = get_card_types()[:10]
    # TEMPORARY. FOR TESTING
    if not Militia in card_types:
        card_types.append(Militia)
    players_info = dict(Jack=Simpleton,
                        Vicky=Victor,
                        The_Rock=Rockefeller,
                        Guy=TheGuy,
                        Dynamite=Napoleon)

    start_game(card_types, players_info)


if __name__ == '__main__':
    main()
