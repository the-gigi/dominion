import cards
import inspect
from cards import *


def get_card_types():
    return [cls for _, cls in inspect.getmembers(cards) if inspect.isclass(cls) and cls != cards.BaseCard]


def count_money(cards):
    amount = 0
    for card in cards:
        if isinstance(card, Gold):
            amount += 3
        elif isinstance(card, Silver):
            amount += 2
        elif isinstance(card, Copper):
            amount += 1
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
