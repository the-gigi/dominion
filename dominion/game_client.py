from dominion import object_model


class GameClient(object_model.GameClient):
    """Game represents the specific game domain

    In this case Dominion

    """
    def __init__(self, game):
        self.game = game

    def play_action_card(self, card_type):
        return self.game.play_action_card(card_type)

    def buy(self, card):
        return self.game.buy(card)

    def done(self):
        self.game.done()
