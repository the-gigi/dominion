from card_util import get_card_types
from computer_players.simpleton import Simpleton
from computer_players.rockefeller import Rockefeller
from game_factory import create_game_engine


def main():
    """ """
    card_types = get_card_types()[:10]
    # players_info = dict(Saar=Simpleton,
    #                     Igig=Simpleton,
    #                     Guuy=Simpleton,
    #                     Liat=Simpleton,
    #                     Ofir=Simpleton)
    players_info = dict(Rocky=Rockefeller,
                        Igig=Simpleton,
                        Sara=Simpleton,)
    game_engine = create_game_engine(card_types, players_info)
    game_engine.run()


if __name__ == '__main__':
    main()
