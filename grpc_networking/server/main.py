from concurrent import futures

import grpc

from grpc_networking.server.dominion_server import DominionServer
from grpc_networking.proto import dominion_pb2_grpc


def main():
    dominion_server = DominionServer()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    dominion_pb2_grpc.add_DominionServerServicer_to_server(dominion_server, server)
    server.add_insecure_port('[::]:50051')
    print('Dominion server is running...')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    main()
