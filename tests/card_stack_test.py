from card_stack import *
import unittest


class TestGame(unittest.TestCase):
    def test_shuffle(self):
        """For each test case:
        1. create card stack
        2. call shuffle() multiple times
        3. check it was shuffled correctly

        test cases:
        empty card stack
        card stack with just one card
        card stack with many cards


        checks:
        1. exact same cards in card stack after shuffle
        2. multiple shuffles result in different ordering (if more than one card type in stack)
        :return:
        """
        card_stack = CardStack()
        for i in range(7):
            card_stack.shuffle()
            self.assertEqual(len(card_stack.cards), 0)

        card_stack = CardStack([Copper()])
        before_shuffle = card_stack.as_dict()
        for i in range(7):
            card_stack.shuffle()
            self.assertEqual(card_stack.as_dict(), before_shuffle)

        card_stack = CardStack([Copper(), Curse(), Silver(), Silver()])
        before_dict = card_stack.as_dict()
        before_cards = card_stack.cards[:]
        shuffle_worked = False
        for i in range(7):
            card_stack.shuffle()
            self.assertEqual(card_stack.as_dict(), before_dict)
            if card_stack.cards != before_cards:
                shuffle_worked = True
        self.assertTrue(shuffle_worked)

if __name__ == '__main__':
    unittest.main()
