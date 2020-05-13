from functools import partial

from dominion import object_model


class GameClient(object_model.GameClient):
    """
    """
    def __init__(self, kube_client, player_name):
        self.kube_client = kube_client
        self.player_name = player_name
        self.patch = partial(self.kube_client.patch_namespaced_custom_object,
                             version='v1',
                             namespace='default',
                             plural='players',
                             name=player_name)

    def play_action_card(self, card):
        """
        Update the spec with:
        play_action_card: card
        """
        self.patch(body=dict(play_action_card=card))
        return True

    def buy(self, card):
        self.patch(body=dict(buy=card))
        return True

    def done(self):
        self.patch(body=dict(done=True))
        return True
