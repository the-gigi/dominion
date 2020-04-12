import object_model


class GameClient(object_model.GameClient):
    """Game represents the specific game domain

    In this case Dominion

    """
    def __init__(self, personal_state, game):
        self.game = game
        self.personal_state = personal_state

    def play_action_card(self, card):
        return self.game.play_action_card(card)

    def buy(self, card):
        return self.game.buy(card)

    def done(self):
        self.game.done()

    # @property
    # def state(self):
    #     return self.state
