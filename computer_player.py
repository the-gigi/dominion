

class ComputerPlayer:
    def __init__(self, name):
        """ """
        self.name = name

    def play(self, game, state):
        """The player has to make one of the actions on the game object

        Some actions are:
        - play card from hand
        - buy cards from thh piles

        If an invalid action is attempted the game object will return an error
        """
        game.end_turn()
