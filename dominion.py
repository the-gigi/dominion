import inspect

import cards
from computer_player import ComputerPlayer
from game import Game
from game_engine import GameEngine


def main():
    """ """
    player_names = ['Bob']
    players = [ComputerPlayer(name) for name in player_names]
    game = Game(player_names)
    game_engine = GameEngine(game, players)
    game_engine.run()


def dump_cards():
    for name, cls in inspect.getmembers(cards):
        if inspect.isclass(cls) and cls != cards.BaseCard:
            print('-' * 10)
            cls().dump()


if __name__ == '__main__':
    main()
