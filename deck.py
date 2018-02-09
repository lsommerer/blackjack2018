from card import Card
from random import randrange


class Deck(list):

    def __init__(self):
        list.__init__(self)
        for suit in Card.suits:
            for name in Card.names:
                card = Card(name, suit)
                self.append(card)

    def __str__(self):
        debugMode = Card.debugMode
        Card.debugMode = True
        deckString = '['
        for card in self:
            deckString += str(card) + ', '
        deckString = deckString[:-2] + "]"
        Card.debugMode = debugMode
        return deckString

    def shuffle(self):
        """Shuffles the deck in place"""
        for pos1 in range(len(self)):
            pos2 = randrange(len(self))
            self[pos1], self[pos2] = self[pos2], self[pos1]

    def draw(self):
        """Returns the top card from the deck; removing it from the deck in the process."""
        if len(self) >= 1:
            card = self.pop()
        else:
            raise ValueError('Not enough cards in the deck to draw')
        return card

    def flip(self):
        """Turn over all the cards in the deck. Useful for testing."""
        for card in self:
            card.flip()


import unittest


class DeckTester(unittest.TestCase):
    string = '[A♣, 2♣, 3♣, 4♣, 5♣, 6♣, 7♣, 8♣, 9♣, 10♣, J♣, Q♣, K♣, A♠, 2♠, 3♠, 4♠, 5♠, 6♠, 7♠, 8♠, 9♠, 10♠, J♠, Q♠, K♠, A♡, 2♡, 3♡, 4♡, 5♡, 6♡, 7♡, 8♡, 9♡, 10♡, J♡, Q♡, K♡, A♢, 2♢, 3♢, 4♢, 5♢, 6♢, 7♢, 8♢, 9♢, 10♢, J♢, Q♢, K♢]'

    def test_str(self):
        deck = Deck()
        self.assertEqual(str(deck), DeckTester.string)

    def test_create_deck(self):
        deck = Deck()
        self.assertEqual(len(deck), 52, 'There should be 52 cards in the deck.')
        deck.flip()
        for cardName in Card.names:
            for suit in Card.suits:
                card = Card(cardName, suit)
                card.flip()
                self.assertEqual(deck.count(card), 1, f'There should be 1 {cardName} in the deck.')

    def test_shuffle(self):
        deck = Deck()
        size = len(deck)
        deck.shuffle()
        self.assertEqual(len(deck), size, "Shuffling shouldn't change deck size")
        self.assertNotEqual(str(deck), DeckTester.string, "Deck doesn't appear shuffled.")
        deck.flip()
        for cardName in Card.names:
            for suit in Card.suits:
                card = Card(cardName, suit)
                card.flip()
                self.assertEqual(deck.count(card), 1, f'There should be 1 {cardName} in the deck.')

    def test_draw(self):
        deck = Deck()
        c = deck.draw()
        c.flip()
        kingOfDiamonds = Card('king', 'diamonds')
        kingOfDiamonds.flip()
        self.assertEqual(c, kingOfDiamonds, 'Top card should be the King of Diamonds.')
        self.assertEqual(len(deck), 51, "There should be 51 cards in the deck after 1 draw.")
        #
        # Draw the rest of the cards from the deck and see if drawing one more raises an exception.
        #
        for _ in range(51):
            c = deck.draw()
        self.assertRaises(ValueError, deck.draw)


if __name__ == '__main__':
    unittest.main(verbosity=2)
