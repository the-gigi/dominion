from dominion_game_engine.cards import *
from computer_players.rockefeller import Rockefeller
from computer_players.victor import Victor
from computer_players.the_guy import TheGuy
from computer_players.napoleon import Napoleon

card_types = [
    Bureaucrat,
    CouncilRoom,
    Festival,
    Library,
    Market,
    Militia,
    Moat,
    Smithy,
    Village,
    Witch]

computer_players = [
    ('Vicky', Victor),
    ('Rocky', Rockefeller),
    ('Guy', TheGuy),
    ('Dynamite', Napoleon),
]