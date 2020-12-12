import copy
import unittest

from dominion_game_engine.cards import Village, Market, Estate
from dominion_game_engine.hand import has_card_types, has_card_type, select_by_name, remove_by_name


class HandTest(unittest.TestCase):
    def setUp(self) -> None:
        self.village1 = Village()
        self.village2 = Village()
        self.market = Market()
        self.hand = [self.village1, self.market, self.village2]

    def test_has_card_type(self):
        self.assertTrue(has_card_type(self.hand, 'Action'))
        self.assertFalse(has_card_type(self.hand, 'Victory'))
        self.assertFalse(has_card_type(self.hand, 'Treasure'))
        self.assertFalse(has_card_type(self.hand, 'Curse'))

    def test_has_card_types(self):
        self.assertTrue(has_card_types(self.hand, ['Action', 'Action', 'Action']))
        self.assertTrue(has_card_types(self.hand, ['Action']))
        self.assertFalse(has_card_types(self.hand, ['Treasure']))
        self.assertFalse(has_card_types(self.hand, ['Action', 'Treasure']))

        self.hand.append(Estate())

        self.assertTrue(has_card_types(self.hand, ['Action', 'Victory']))

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