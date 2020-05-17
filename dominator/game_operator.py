import asyncio
import kopf

from dominator.game import Game

game = None
players = []


@kopf.on.create('dominion.org', 'v1', 'games')
@kopf.on.resume('dominion.org', 'v1', 'games')
def on_create_game(body, name, namespace, logger, **kwargs):
    print(f'A game was created with body: {body}')
    global game
    if game is not None:
        return

    game = Game(name, body['spec']['numPlayers'])


@kopf.on.create('dominion.org', 'v1', 'players')
def on_create_player(body, name, namespace, logger, **kwargs):
    """Update game by adding the player name to its status

    """
    print(f'A player was created with body: {body}')
    if game is None:
        return

    try:
        game.join(name)
    except Exception as e:
        print(e)
    print(game.players)

@kopf.on.update('dominion.org', 'v1', 'games')
def on_game_update(spec, status, namespace, logger, **kwargs):
    pass


@kopf.on.update('dominion.org', 'v1', 'players')
def on_player_update(spec, status, namespace, logger, **kwargs):
    pass


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(kopf.operator())


if __name__ == '__main__':
    main()
