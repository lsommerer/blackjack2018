from card import Card
from cardcollection import CardCollection


class Deck(CardCollection):

    def __init__(self):
        super().__init__()
        for suit in Card.suits:
            for name in Card.names:
                card = Card(name, suit)
                self.append(card)

    def stack(self, deckFile='stacked-deck.txt'):
        """Stack the deck. Also useful for testing."""
        self.clear()
        with open(deckFile,'r') as file:
            for line in file:
                value, suit = line.split(" of ")
                card = Card(value, suit.strip())
                self.append(card)


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
