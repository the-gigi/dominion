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
