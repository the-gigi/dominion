from dominion import object_model
from dominator.player_custom_resource import PlayerCustomResource


class GameClient(object_model.GameClient):
    """
    """
    def __init__(self, player_cr: PlayerCustomResource):
        self.player_cr = player_cr

    def play_action_card(self, card_type):
        """
        Update the spec with:
        play_action_card: card
        """
        self.player_cr.patch(body=dict(play_action_card=card_type))
        return True

    def buy(self, card):
        self.player_cr.patch(body=dict(buy=card))
        return True

    def done(self):
        self.player_cr.patch(body=dict(done=True))
        return True

    @property
    def state(self):
        return self.player_cr.status.get('state', {})
