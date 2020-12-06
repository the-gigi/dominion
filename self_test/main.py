from computer_players.stay_at_home_son import StayAtHomeSon
from dominion_game_engine.game_factory import start_game
from dominion_game_engine.cards import *
from computer_players.rockefeller import Rockefeller
from computer_players.victor import Victor
from computer_players.the_guy import TheGuy
from computer_players.napoleon import Napoleon

# card_types = [
#     #Adventurer,
#     Bureaucrat,
#     #Chancellor,
#     CouncilRoom,
#     Festival,
#     Library,
#     Market,
#     Militia,
#     Moat,
#     Smithy,
#     #Spy,
#     #Thief,
#     Village,
#     Witch]

card_types = [
    #Adventurer,
    #Bureaucrat,
    #Chancellor,
    Cellar,
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
                    Dynamite=(Napoleon, None),
                    Zak_Galafinakis=(StayAtHomeSon, None))


def main():
    """ """
    start_game(card_types, players_info)


if __name__ == '__main__':
    main()
