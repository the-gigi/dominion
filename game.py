

class Game:
    def __init__(self):
        # The players
        self.players = []

        # The active player
        self.active_player

        # A dictionary of the kingdom cards <card_type>:<number of remaining cards>
        self.supply = {}

        # Trashed cards go here
        self.trash = []

        self.state = GameState()

    def play_action_card(self, card):
        """ """

    def buy(self, card):
        """ """

    def done(self, card):
        """ """
