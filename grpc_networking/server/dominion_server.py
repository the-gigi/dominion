import json
import random
from dataclasses import dataclass

import queue
from functools import partial
from threading import Thread

from dominion_game_engine import game_factory
from dominion_grpc_proto.dominion_pb2 import Message, Response
from dominion_grpc_proto.dominion_pb2_grpc import DominionServerServicer

try:
    from grpc_networking.server import config
    from grpc_networking.server.player import Player
except ImportError:
    import config
    from player import Player

MAX_PLAYER_COUNT = 4


@dataclass
class PlayerInfo:
    name: str
    queue: queue.Queue
    peer: str


class DominionServer(DominionServerServicer):
    def __init__(self):
        self.players = {}
        self.game_started = False
        self.game_client = None
        self.response = (None, False)

    def attach_game_client(self, game_client):
        self.game_client = game_client

    def _join(self, req, ctx):
        names = [p.name for p in self.players.values()]
        name = req.name
        while name in names:
            name += str(random.randint(1, 9))

        peer = ctx.peer()
        if peer in self.players:
            q = self.players[peer].queue
            q.put(Message(type='error', data='already joined'))
        pi = PlayerInfo(name, queue.Queue(), peer)
        self.players[peer] = pi
        pi.queue.put(Message(type='ack', data=json.dumps(dict(name=pi.name))))
        print(f'Player {name} joined!')
        return pi.queue

    def _prepare_player_info(self):
        players_info = {}
        for p in self.players.values():
            players_info[p.name] = (partial(Player, queue=p.queue), ())
        return players_info

    def start_game(self, player_name):
        """ """
        if self.game_started:
            return
        self.game_started = True
        print('Game started by ', player_name)
        players_info = self._prepare_player_info()
        computer_players = self.get_computer_players()
        for name, player in computer_players:
            players_info[name] = (player, ())

        # Send 'game start' event to all players with cards and player names
        player_names = [p.name for p in self.players.values()] + [name for name, _ in computer_players]
        card_names = [c.Name() for c in config.card_types]
        for p in self.players.values():
            data = dict(event='game start',
                        card_names=card_names,
                        player_names=player_names)
            p.queue.put(Message(type='on_game_event',
                                data=json.dumps(data)))

        Thread(target=game_factory.start_game, args=(config.card_types, players_info, self)).start()

    def get_computer_players(self):
        """ """
        n = MAX_PLAYER_COUNT - len(self.players)
        random.shuffle(config.computer_players)
        return config.computer_players[:n]

    # DominionServer proto service
    def Join(self, player_info, ctx):
        q = self._join(player_info, ctx)
        print(f'[{player_info.name}] Waiting for message to send on queue {id(q)}')
        while True:
            message = q.get()
            yield message

    def Start(self, player_info, ctx):
        try:
            self.start_game(player_info.name)
            return Response(ok=True)
        except Exception as e:
            return Response(ok=False, error=str(e))

    def PlayCard(self, card, ctx):
        peer = ctx.peer()
        if peer not in self.players:
            print('Unknown player:', peer)
            return Response(ok=False)

        self.game_client.play_action_card(card)
        return Response(ok=True)

    def Buy(self, card, ctx):
        peer = ctx.peer()
        if peer not in self.players:
            print('Unknown player:', peer)
            return Response(ok=False, error='Unknown player')

        self.game_client.buy(card)
        return Response(ok=True)

    def Done(self, req, ctx):
        self.game_client.done()
        return Response(ok=True)

    def Respond(self, response, ctx):
        peer = ctx.peer()
        if peer not in self.players:
            print('Unknown player:', peer)
            return Response(ok=False)

        Player.response = response
        return Response(ok=True)
