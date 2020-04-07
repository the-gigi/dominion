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

    def test_pop(self):
        """
        create card stack
        call pop()
        check if the correct number of cards were popped

        test cases:
        0 cards in stack
            ask for 0
            ask for more
        1 card in stack
            ask for less than 1
            ask for 1
            ask for more
        many cards in stack
            ask for less
            ask for the stack
            ask for more

        checks:
        :return:
        """
        # try to pop zero cards from an empty stack
        card_stack = CardStack()
        self.assertEqual(len(card_stack.cards), 0)
        cards = card_stack.pop(0)
        self.assertEqual(len(cards), 0)

        # try to pop a card from an empty stack
        self.assertEqual(len(card_stack.cards), 0)
        self.assertRaises(RuntimeError, card_stack.pop, 1)

        # try to pop zero cards from stack with one card
        card_stack = CardStack([Copper()])
        self.assertEqual(len(card_stack.cards), 1)
        cards = card_stack.pop(0)
        self.assertEqual(len(cards), 0)
        self.assertEqual(len(card_stack.cards), 1)

        # try to pop one card from stack with one card
        self.assertEqual(len(card_stack.cards), 1)
        cards = card_stack.pop(1)
        self.assertEqual(len(cards), 1)
        self.assertEqual(len(card_stack.cards), 0)
        self.assertTrue(isinstance(cards[0], Copper))

        # try to pop more than one card from a stack with one card
        card_stack = CardStack([Copper()])
        self.assertEqual(len(card_stack.cards), 1)
        self.assertRaises(RuntimeError, card_stack.pop, 2)

        # try to pop less than the amount of cards from a stack with many cards
        card_stack = CardStack([Copper(), Silver(), Gold()])
        self.assertEqual(len(card_stack.cards), 3)
        cards = card_stack.pop(2)
        self.assertEqual(len(cards), 2)
        self.assertEqual(len(card_stack.cards), 1)
        self.assertTrue(isinstance(cards[0], Copper))
        self.assertTrue(isinstance(cards[1], Silver))
        self.assertTrue(isinstance(card_stack.cards[0], Gold))

        # try to pop the same amount of cards from a stack with many cards
        card_stack = CardStack([Copper(), Silver(), Gold()])
        self.assertEqual(len(card_stack.cards), 3)
        cards = card_stack.pop(3)
        self.assertEqual(len(cards), 3)
        self.assertEqual(len(card_stack.cards), 0)
        self.assertTrue(isinstance(cards[0], Copper))
        self.assertTrue(isinstance(cards[1], Silver))

        # try to pop more cards from a stack with many cards
        card_stack = CardStack([Copper(), Silver(), Gold()])
        self.assertEqual(len(card_stack.cards), 3)
        self.assertRaises(RuntimeError, card_stack.pop, 4)
        self.assertTrue(isinstance(card_stack.cards[0], Copper))
        self.assertTrue(isinstance(card_stack.cards[1], Silver))
        self.assertTrue(isinstance(card_stack.cards[2], Gold))

if __name__ == '__main__':
    unittest.main()
