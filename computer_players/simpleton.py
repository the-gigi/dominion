from dominion.object_model import BasePlayer


class Simpleton(BasePlayer):
    def play(self):
        """The player has to make one of the actions on the game object

        Some actions are:
        - play card from hand
        - buy cards from the piles

        If an invalid action is attempted the game object will return an error
        """
        self.game_client.done()

    def respond(self, request, *args):
        return


