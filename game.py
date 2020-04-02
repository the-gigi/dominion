class Game:
    """Game represents the specific game domain

    In this case Dominion

    """

    def __init__(self, active_player_index):
        # The players
        self.player_states = []

        # The active player
        self.active_player_index = active_player_index

        # A dictionary of the kingdom cards <card_type>:<number of remaining cards>
        self.supply = {}

        # Trashed cards go here
        self.trash = []

    @property
    def player_state(self):
        return self.player_states[self.active_player]

    @property
    def active_player(self):
        return self.active_player_index

    @active_player.setter
    def active_player(self, player_index):
        self.active_player_index = player_index

    def verify_action(self, card):
        """verify the player has the card in hand and has at least one action
        """
        raise NotImplementedError

    def verify_buy(self, card):
        """verify the player has enough money and has at least one buy
        """
        raise NotImplementedError

    # Player interface
    def play_action_card(self, card):
        """ """
        raise NotImplementedError

    def buy(self, card):
        """ """
        raise NotImplementedError

    def end_turn(self):
        """ """
        self.player_state.end_turn()
