from time import sleep

from pod_six_net.server.dominion_server import DominionServer


def main():
    server = DominionServer()
    while True:
        server.Pump()
        sleep(0.0001)


if __name__ == '__main__':
    main()
