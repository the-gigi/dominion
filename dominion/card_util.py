from collections import defaultdict

from dominion import cards
import inspect
from dominion.cards import *


def get_card_types():
    return [cls for _, cls in inspect.getmembers(cards) if inspect.isclass(cls) and cls != cards.BaseCard]


def as_dict(cards):
    """
    Create a dict where the keys are card class and the value is the number of cards of this type
    Iterate over all the cards
    For each card type increment the value in the dictionary

    :return dict
    """
    dd = defaultdict(int)
    for card in cards:
        dd[repr(card)] += 1
    return dd


def count_points(cards):
    """Count the total victory points in
       the player's hand, deck and discard pile

       return the number of victory points
    """
    vp = 0
    for card in cards:
        vp += card.Points
    return vp


def count_money(cards, only_treasures=True):
    amount = 0
    for card in cards:
        if only_treasures and card.Type != 'Treasure':
            continue
        amount += card.Coins
    return amount


def setup_piles(card_types, num_players):
    copper_count = 60
    silver_count = 40
    gold_count = 30

    piles = {c: 13 for c in card_types}
    piles[Copper] = copper_count - num_players * 7
    piles[Silver] = silver_count
    piles[Gold] = gold_count

    piles[Estate] = 8 if num_players == 2 else 12
    piles[Duchy] = 8 if num_players == 2 else 12
    piles[Province] = 8 if num_players == 2 else 12
    piles[Curse] = (num_players - 1) * 10
    return piles
