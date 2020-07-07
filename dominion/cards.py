class BaseCard:
    Type = ''
    Text = ''
    Cost = 0
    Coins = 0
    Points = 0
    Reaction = False

    def __init__(self):
        # self.Name = self.__class__.__name__
        self.Image = f'images/{self.Name().lower()}.jpg'

    def __repr__(self):
        return f'{type(self).__name__}: {id(self)}'

    @classmethod
    def Name(cls):
        return cls.__name__

    def dump(self):
        for a in 'name type text cost coins points reaction'.split():
            print(f'{a.capitalize()}: {self.__getattribute__(a.capitalize())}')

    def as_dict(self):
        return dict(
            name=self.__class__.__name__,
            type=self.Type,
            text=self.Text,
            cost=self.Cost,
            coins=self.Coins,
            points=self.Points,
            reaction=self.Reaction
        )


class Estate(BaseCard):
    Type = 'Victory'
    Text = "1 VP"
    Cost = 2
    Points = 1


class Duchy(BaseCard):
    Type = 'Victory'
    Text = "3 VP"
    Cost = 5
    Points = 3


class Province(BaseCard):
    Type = 'Victory'
    Text = "6 VP"
    Cost = 8
    Points = 6


class Curse(BaseCard):
    Type = 'Curse'
    Text = "-1 VP"
    Cost = 0
    Points = -1


class Copper(BaseCard):
    Type = 'Treasure'
    Text = "💰1"
    Coins = 1
    Cost = 0


class Silver(BaseCard):
    Type = 'Treasure'
    Text = "💰2"
    Coins = 2
    Cost = 3


class Gold(BaseCard):
    Type = 'Treasure'
    Text = "💰3"
    Coins = 3
    Cost = 6


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
    Coins = 2
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
    +$2
    """
    Coins = 2
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
    Coins = 2
    Cost = 4
    Reaction = False


class Moat(BaseCard):
    Type = 'Action'
    Text = """
    +2 Cards

    When another player plays an Attack card, you may first
    reveal this from your hand, to be unaffected by it.     
    """
    Cost = 2
    Reaction = True


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
