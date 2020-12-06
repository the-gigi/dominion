import copy
import unittest

from dominion_game_engine.cards import Village, Market
from dominion_game_engine.hand import has_card_types, has_card_type, select_by_name, remove_by_name


class HandTest(unittest.TestCase):
    def setUp(self) -> None:
        self.village1 = Village()
        self.village2 = Village()
        self.market = Market()
        self.hand = [self.village1, self.market, self.village2]

    def test_has_card_type(self):
        self.assertFalse(has_card_type(self.hand, 'WITCH'))
        self.assertFalse(has_card_type(self.hand, 'VILLAGE'))
        self.assertFalse(has_card_type(self.hand, 'MARKET'))

    def test_has_card_types(self):
        # Non-existent card type - should return False
        self.assertFalse(has_card_types(self.hand, ['WITCH']))

        # Too many card types - should return False
        self.assertFalse(has_card_types(self.hand, ['MARKET', 'MARKET']))

        # Subset of cards - should return True
        self.assertFalse(has_card_types(self.hand, ['VILLAGE', 'VILLAGE']))

        # Correct number of same card - should return True
        self.assertFalse(has_card_types(self.hand, ['VILLAGE', 'VILLAGE']))

        # Multiple correct card types - should return True
        self.assertFalse(has_card_types(self.hand, ['VILLAGE', 'MARKET']))

    def test_select_by_name(self):
        selected = select_by_name(self.hand, ['Witch'])
        self.assertEqual(selected, [])

        selected = select_by_name(self.hand, ['Village'])
        self.assertEqual(selected, [self.village1])

        selected = select_by_name(self.hand, ['Village', 'Village'])
        self.assertEqual(selected, [self.village1, self.village2])

        selected = select_by_name(self.hand, ['Market'])
        self.assertEqual(selected, [self.market])

        selected = select_by_name(self.hand, ['Village', 'Village', 'Market'])
        self.assertEqual(selected, [self.market, self.village1, self.village2])

    def test_remove_by_name(self):
        hand = copy.deepcopy(self.hand)
        remove_by_name(self.hand, ['Witch'])
        self.assertListEqual(self.hand, hand)

        remove_by_name(self.hand, ['Village'])
        self.assertEqual(self.hand, [self.market, self.village2])