import grpc

from grpc_networking.proto import dominion_pb2_grpc
from grpc_networking.proto.dominion_pb2 import PlayerInfo


def join(stub):
    messages = stub.Join(PlayerInfo(name='dummy'))
    for message in messages:
        print(message)
    print('join() done.')


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = dominion_pb2_grpc.DominionServerStub(channel)
        join(stub)
        print('after join()')


if __name__ == '__main__':
    run()
