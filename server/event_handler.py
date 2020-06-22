from abc import ABCMeta, abstractmethod


class EventHandler(metaclass=ABCMeta):
    @abstractmethod
    def on_start(self, channel):
        pass

    @abstractmethod
    def on_join(self, channel, name):
        pass

    @abstractmethod
    def on_play_action_card(self, channel, card):
        pass

    @abstractmethod
    def on_buy(self, channel, card):
        pass

    @abstractmethod
    def on_done(self, channel):
        pass

    @abstractmethod
    def on_respond(self, channel, response):
        pass
