import random
from dataclasses import dataclass

import grpc
import queue
from concurrent import futures

from grpc_networking.proto import dominion_pb2_grpc
from grpc_networking.proto.dominion_pb2 import Message
from grpc_networking.proto.dominion_pb2_grpc import DominionServerServicer


@dataclass
class PlayerInfo:
    name: str
    queue: queue.Queue
    peer: str


class Server(dominion_pb2_grpc.DominionServerServicer):
    def __init__(self):
        self.players = {}

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
        pi.queue.put(Message(type='ack', data=f'name: {pi.name}'))

        return pi.queue

    def Join(self, req, ctx):
        q = self._join(req, ctx)
        while True:
            message = q.get()
            yield message


def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    dominion_pb2_grpc.add_DominionServerServicer_to_server(Server(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    main()
