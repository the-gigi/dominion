import asyncio
import kopf

from dominator.game import Game

game = None
pending_players = []


@kopf.on.create('dominion.org', 'v1', 'games')
@kopf.on.resume('dominion.org', 'v1', 'games')
def on_create_game(body, name, namespace, logger, **kwargs):
    print(f"A {body['spec']['numPlayers']}-players game was created : {name}")
    global game
    if game is not None:
        return

    game = Game(name, body['spec']['numPlayers'])
    for name in pending_players[:game.num_players]:
        print(f'A player joined the game: {name}')
        game.join(name)


@kopf.on.create('dominion.org', 'v1', 'players')
@kopf.on.resume('dominion.org', 'v1', 'players')
def on_create_player(body, name, namespace, logger, **kwargs):
    """Update game by adding the player name to its status

    """
    if game is None:
        print(f'A player was added to pending players: {name}')
        pending_players.append(name)
        return

    print(f'A player joined the game: {name}')
    game.join(name)


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
