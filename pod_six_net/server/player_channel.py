from PodSixNet.Channel import Channel

from pod_six_net.server.event_handler import EventHandler


class PlayerChannel(Channel):
    def attach_event_handler(self, event_handler: EventHandler):
        self.event_handler = event_handler

    def Network(self, data):
        print(data)

    def Network_join(self, data):
        self.event_handler.on_join(self, data['name'])

    def Network_start(self, data):
        self.event_handler.on_start(self)

    def Network_play_action_card(self, data):
        self.event_handler.on_play_action_card(self, data['card'])

    def Network_buy(self, data):
        self.event_handler.on_buy(self, data['card'])

    def Network_done(self, data):
        self.event_handler.on_done(self)

    def Network_respond(self, data):
        self.event_handler.on_response(self, data['response'])
