from dominion_game_engine.cards import *
from computer_players.rockefeller import Rockefeller
from computer_players.victor import Victor
from computer_players.the_guy import TheGuy
from computer_players.napoleon import Napoleon
from computer_players.stay_at_home_son import StayAtHomeSon
from computer_players.robin_hood import RobinHood

card_types = [
    Artisan,
    Bandit,
    Bureaucrat,
    # CouncilRoom,
    Festival,
    Library,
    # Market,
    Militia,
    # Mine,
    # Moat,
    Remodel,
    Sentry,
    Smithy,
    ThroneRoom,
    # Village,
    Workshop,
    # Vassal,
]

computer_players = [
    ('Archy', RobinHood),
    # ('Vicky', Victor),
    # ('Rocky', Rockefeller),
    #('Guy', TheGuy),
    #('Dynamite', Napoleon),
    #('Zuck', StayAtHomeSon),
]

max_player_count = 2