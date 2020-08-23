from collections import Counter
from typing import List

from dominion_game_engine.cards import BaseCard

Hand = List[BaseCard]


def has_card_type(hand, card_type: str):
    return any(c.Type == card_type for c in hand)


def has_card_types(hand, card_types: List[str]):
    hand_counter = Counter(c.Type for c in hand)
    req_counter = Counter(card_types)
    for card_type, count in req_counter:
        if count < hand_counter[card_type]:
            return False

    return True


def select_by_type(hand, card_types: List[str]):
    selected = []
    sorted_hand = sorted(hand, key=lambda c: c.Type)
    sorted_card_types = sorted(card_types)
    i = 0
    for t in sorted_card_types:
        c = sorted_hand[i]
        if sorted_hand[i].Type == t:
            selected.append(c)
            i += 1
        if sorted_hand[i].Type > t:
            raise RuntimeError(f'type {t} missing')

    return selected
