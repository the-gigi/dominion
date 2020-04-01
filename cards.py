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


class Bureaucrat(BaseCard):
    Type = 'Action'
    Text = """
    Gain a silver card; put it on top of your deck.
    Each other player reveals a Victory card from
    his hand and puts it on top of his deck (or reveals
    a hand with no Victory cards).
    """
    Cost = 4
    Reaction = False


class Chancellor(BaseCard):
    Type = 'Action'
    Text = """
    +$2
    
    You may immediately put your deck into your discard pile.
    """
    Cost = 3
    Reaction = False


class CouncilRoom(BaseCard):
    Type = 'Action'
    Text = """
    +4 Cards
    +1 Buy

    Each other player draws a card.
    """
    Cost = 5
    Reaction = False


class Festival(BaseCard):
    Type = 'Action'
    Text = """
    +2 Actions
    +1 Buy
    +2 Coins
    """
    Cost = 5
    Reaction = False


class Library(BaseCard):
    Type = 'Action'
    Text = """
    Draw until you have 7 cards in hand. You may set aside
    any Action cards drawn this way, as you draw them;
    discard the set aside cards after you finish drawing.
    """
    Cost = 5
    Reaction = False


class Militia(BaseCard):
    Type = 'Action'
    Text = """
    +$2
    
    Each player discards down to 3 cards in his hand.
    """
    Cost = 4
    Reaction = False


class Spy(BaseCard):
    Type = 'Action'
    Text = """
    +1 Card
    +1 Action
    
    Each player (including you) reveals the top card of his deck
    and either discards it or puts it back, your choice.
    """
    Cost = 4
    Reaction = False


class Thief(BaseCard):
    Type = 'Action'
    Text = """
    Each other player reveals the top 2 cards of his deck.
    If they revealed any Treasure cards, they trash one of them that you choose.
    You may gain any or all of these trashed cards.
    They discard the other revealed cards.
    """
    Cost = 4
    Reaction = False


class Village(BaseCard):
    Type = 'Action'
    Text = """
    +1 Card
    +2 Actions
    """
    Cost = 3
    Reaction = False