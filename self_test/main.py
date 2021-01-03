from computer_players.stay_at_home_son import StayAtHomeSon
from dominion_game_engine.game_factory import start_game
from dominion_game_engine.cards import *
from computer_players.rockefeller import Rockefeller
from computer_players.victor import Victor
from computer_players.the_guy import TheGuy
from computer_players.napoleon import Napoleon
from computer_players.robin_hood import RobinHood

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
    # Adventurer,
    Bandit,
    # Bureaucrat,
    # Chancellor,
    Cellar,
    CouncilRoom,
    Festival,
    Library,
    Market,
    Militia,
    Moat,
    Smithy,
    # Spy,
    # Thief,
    ThroneRoom,
    Village,
    Witch,
    Workshop]

players_info = dict(Vicky=(Victor, None),
                    Guy=(TheGuy, None),
                    #The_Rock=(Rockefeller, None),
                    Dynamite=(Napoleon, None),
                    #Zak_Galafinakis=(StayAtHomeSon, None),
                    Robin=(RobinHood, None),
                    )


def main():
    """ """
    start_game(card_types, players_info)


if __name__ == '__main__':
    main()
