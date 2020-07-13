from dominion.game_factory import start_game
from dominion.cards import *
from computer_players.rockefeller import Rockefeller
from computer_players.victor import Victor
from computer_players.the_guy import TheGuy
from computer_players.napoleon import Napoleon

card_types = [
    #Adventurer,
    Bureaucrat,
    #Chancellor,
    CouncilRoom,
    Festival,
    Library,
    Market,
    Militia,
    Moat,
    Smithy,
    #Spy,
    #Thief,
    Village,
    Witch]

players_info = dict(Vicky=(Victor, None),
                    The_Rock=(Rockefeller, None),
                    Guy=(TheGuy, None),
                    Dynamite=(Napoleon, None))


def main():
    """ """
    start_game(card_types, players_info)


if __name__ == '__main__':
    main()
