from collections import Counter
from typing import List

from dominion_game_engine.cards import BaseCard

Hand = List[BaseCard]


def has_card_type(hand, card_type: str):
    return any(c.Type == card_type for c in hand)


def has_card_types(hand, card_types: List[str]) -> bool:
    hand_counter = Counter(c.Type for c in hand)
    req_counter = Counter(card_types)
    for card_type, count in req_counter.items():
        if count < hand_counter[card_type] or hand_counter[card_type] == 0:
            return False

    return True


def select_by_name(hand, card_names: List[str]) -> List[BaseCard]:
    selected = []
    sorted_hand = sorted(hand, key=lambda c: c.Name())
    sorted_card_names = sorted(card_names)
    i = 0
    for card_name in sorted_card_names:
        while i < len(sorted_hand) and sorted_hand[i].Name() < card_name :
            i += 1

        # missing card name
        if i == len(sorted_hand):
            return []

        card = sorted_hand[i]
        if card.Name() == card_name:
            selected.append(card)
            i += 1
        else:
            raise RuntimeError(f'card name {card_name} is missing')

    return selected


def remove_by_name(hand, card_names: List[str]):
    for card_name in card_names:
        for card in hand:
            if card.Name() == card_name:
                hand.remove(card)
                break
