class BaseCard:
    Type = ''
    Text = ''
    Cost = 0
    Coins = 0
    Points = 0
    Reaction = False

    def __init__(self,
                 reaction=False):
        self.Name = self.__class__.__name__
        self.Image = f'images/{self.Name.lower()}.jpg'

    def dump(self):
        for a in 'name type text cost coins points reaction'.split():
            print(f'{a.capitalize()}: {self.__getattribute__(a.capitalize())}')


class Estate(BaseCard):
    Type = 'Victory'
    Text = "1 VP"
    Cost = 2
    VictoryPoints = 1


class Copper(BaseCard):
    Type = 'Treasure'
    Text = "1 Copper"
    Coins = 1


class Moat(BaseCard):
    Type = 'Action'
    Text = """
    +2 Cards
    
    When another player plays an Attack card, you may first
    reveal this from your hand, to be unaffected by it.     
    """
    Cost = 2
    Reaction = True
