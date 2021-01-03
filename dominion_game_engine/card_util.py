from collections import defaultdict
from typing import Dict

from dominion_game_engine import cards
import inspect
from dominion_game_engine.cards import *

card_attributes = [k for k,v in BaseCard.__dict__.items() if not k.startswith('__') and not callable(v) and k != 'Name']


def get_card_types():
    return {cls.__name__: cls for _, cls in inspect.getmembers(cards) if inspect.isclass(cls) and cls != cards.BaseCard}


def serialize_card_types():
    card_types = get_card_types()
    return {name: {a: getattr(card_type, a) for a in card_attributes} for name, card_type in card_types.items()}


def get_card_class(card_name):
    return get_card_types()[card_name]


def as_dict(cards):
    """
    Create a dict where the keys are card class and the value is the number of cards of this type
    Iterate over all the cards
    For each card type increment the value in the dictionary

    :return dict
    """
    dd = defaultdict(int)
    for card in cards:
        dd[card.__class__.__name__] += 1
    return dict(dd)


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


def setup_piles(card_types, num_players) -> Dict[str, int]:
    copper_count = 60
    silver_count = 40
    gold_count = 30

    piles = {c.Name(): 13 for c in card_types}
    piles['Copper'] = copper_count - num_players * 7
    piles['Silver'] = silver_count
    piles['Gold'] = gold_count

    piles['Estate'] = 8 if num_players == 2 else 12
    piles['Duchy'] = 8 if num_players == 2 else 12
    piles['Province'] = 8 if num_players == 2 else 12
    piles['Curse'] = (num_players - 1) * 10
    return piles
