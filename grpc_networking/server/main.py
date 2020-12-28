from concurrent import futures

import grpc

try:
    from grpc_networking.server.dominion_server import DominionServer
except ImportError:
    from dominion_server import DominionServer

from dominion_grpc_proto import dominion_pb2_grpc

# The default gRPC port of 50051 is blocked on windows
# see https://medium.com/@Bartleby/ports-are-not-available-listen-tcp-0-0-0-0-3000-165892441b9d
port = 55555


def main():
    dominion_server = DominionServer()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    dominion_pb2_grpc.add_DominionServerServicer_to_server(dominion_server, server)
    server.add_insecure_port(f'[::]:{port}')
    print('Dominion server is running...')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    main()
