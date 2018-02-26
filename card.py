from errors import RuleError


class Card(object):
    #
    # In addition to instance variables, there are also class variables
    # these variables are shared by all instances of the class (all objects).
    # Lets use some of them below:
    #
    suits = ['clubs', 'spades', 'hearts', 'diamonds']
    unicode = ['\u2663', '\u2660', '\u2661', '\u2662']
    #
    # This next bit is called a dictionary in Python(because you can look stuff up)
    # but it is called other things in other languages for instance, you might
    # hear it called a "hash table" which actually describes how it is implemented,
    # or hear it pretty generically as a "mapping".
    #
    # There are other ways to create a dictionary, but if you have two lists this
    # is pretty easy:
    #
    unicodeDict = dict(zip(suits, unicode))
    #
    # This is another way to do exactly the same thing:
    #
    # unicodeDict = {'clubs':'\u2663', 'spades':'\u2660', 'hearts':'\u2661', 'diamonds':'\u2662'}
    #
    # You use a dictionary like this: clubUnicode = unicodeDict['clubs']
    #
    # You can think of them like lists where you refer to the items in the list
    # by name instead of number. The plus side to that is you don't have to know
    # where something is in the dictionary. You just hae to know that it is in
    # there.
    #
    # The two parts of a dictionary entry are called the "key" and the "value".
    # The key is the first part and it's how to refer to the thing in the dictionary.
    # The value is the second part. It is the data. It can be any type of data.
    #

    names = ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king']
    shortNames = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    shortNameDict = dict(zip(names, shortNames))

    hardValues = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
    softValues = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

    hardValueDict = dict(zip(names, hardValues))
    softValueDict = dict(zip(names, softValues))

    ranks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10 , 11, 12, 13]
    rankDict = dict(zip(names, ranks))

    useUnicode = True
    #
    # Debug Mode:
    #   True: cards can be printed even if they are not "showing".
    #   false: DEFAULT cards display '[flipped over]' if they are printed while not showing.
    #
    debugMode = False
    #
    # Note on is_showing():
    #
    #   It is the responsibility of the object calling Card object getters to ask the card
    #   if it is currently visible before asking for any specific information about the card.
    #
    #   correct:  if dealerCard.is_showing() and dealerCard.is_ace():
    #                   dealer.offer_insurance()
    #
    #   incorrect:  if dealerCard.is_ace():
    #                   dealer.offer_insurance()
    #
    #   if you ask for information about a card that is not showing, a RulesError exception
    #   will be raised.
    #

    def __init__(self, name, suit):
        #
        # Check that the name is a legal name.
        #
        if name.lower() in Card.names:
            self.__name = name.lower()
            self.__shortName = Card.shortNameDict[self.__name]
        #
        # Or that name is a legal short name, just in case.
        #
        elif name.upper() in Card.shortNames:
            name = Card.names[Card.shortNames.index(name.upper())]
            self.__name = name.lower()
            self.__shortName = Card.shortNameDict[self.__name]
        else:
            raise TypeError(name + ' is not a valid card name.')
        #
        # Check that the suit is legal
        #
        if suit.lower() in Card.suits:
            self.__suit = suit.lower()
        else:
            raise TypeError(suit + ' is not a valid card suit.')
        #
        # Check if it is a facecard
        #
        if self.__name in ['jack', 'queen', 'king']:
            self.__isFacecard = True
        else:
            self.__isFacecard = False
        #
        # Check if it is an ace
        #
        if self.__name == 'ace':
            self.__isAce = True
        else:
            self.__isAce = False
        #
        # A few more settings
        #
        self.__isShowing = False
        self.__rank = Card.rankDict[self.__name]
        self.__hardValue = Card.hardValueDict[self.__name]
        self.__softValue = Card.softValueDict[self.__name]

    def __str__(self):
        if Card.useUnicode:
            string = f'{self.__shortName}{Card.unicodeDict[self.__suit]}'
        else:
            string = f'{self.__name.capitalize()} of {self.__suit.capitalize()}'
        if not self.__isShowing and not Card.debugMode:
            string = '[face down]'
        return string

    def __repr__(self):
        return f"Card('{self.__name}','{self.__suit}')"

    def __eq__(self, other):
        #
        # This special method is called when the == operator is invoked.
        #
        return self.same_rank(other) and self.same_suit(other)

    def __lt__(self,other):
        return self.__rank < other.__rank

    def flip(self):
        """Flips the card over from 'showing' to 'not showing' or visa versa."""
        self.__isShowing = not self.__isShowing
        return self

    def is_showing(self):
        """Returns True if the card is face-up and can be seen."""
        return self.__isShowing

    def same_suit(self, other):
        """Returns True if both cards are the same suit."""
        if not self.is_showing() and not other.is_showing():
            raise RuleError('card is not showing, you can not use same_suit()')
        return self.suit == other.suit

    def same_rank(self, other):
        """Returns True if both cards are the same rank."""
        if not self.is_showing() and not other.is_showing():
            raise RuleError('card is not showing, you can not use same_rank()')
        return self.rank == other.rank

    def get_is_facecard(self):
        """Returns True if the card is a facecard."""
        if not self.is_showing():
            raise RuleError('card is not showing, you can not use is_face_card()')
        return self.__isFacecard

    def get_is_ace(self):
        """Returns True if the card is an ace."""
        if not self.is_showing():
            raise RuleError('card is not showing, you can not use is_ace()')
        return self.__isAce


    def get_hard_value(self):
        """Returns the hard value of the card."""
        if not self.is_showing():
            raise RuleError('card is not showing, you can not use hard_value()')
        return self.__hardValue

    def get_soft_value(self):
        """Returns the soft value of the card."""
        if not self.is_showing():
            raise RuleError('card is not showing, you can not use hard_value()')
        return self.__softValue

    def get_suit(self):
        """Returns the suit of the card."""
        if not self.is_showing():
            raise RuleError('card is not showing, you can not use suit()')
        return self.__suit

    def get_name(self):
        """Returns the name of the card."""
        if not self.is_showing():
            raise RuleError('card is not showing, you can not use name()')
        return self.__name

    def get_rank(self):
        """Returns the rank of the card."""
        if not self.is_showing():
            raise RuleError('card is not showing, you can not use rank()')
        return self.__rank

    isFacecard = property(get_is_facecard)
    isAce = property(get_is_ace)
    hardValue = property(get_hard_value)
    softValue = property(get_soft_value)
    suit = property(get_suit)
    name = property(get_name)
    rank = property(get_rank)


import unittest

class CardTester(unittest.TestCase):

    def test_is_showing(self):
        c = Card('ace', 'spades')
        #
        # Turn card face up (they start face down).
        #
        c.flip()
        self.assertTrue(c.is_showing())
        self.assertTrue(c.isAce)
        self.assertFalse(c.isFacecard)
        self.assertEqual(c.rank, 1)
        self.assertEqual(c.name, 'ace')
        self.assertEqual(c.suit, 'spades')
        self.assertEqual(c.softValue, 11)
        self.assertEqual(c.hardValue, 1)
        #
        # Turn card face down.
        #
        c.flip()
        self.assertFalse(c.is_showing())
        with self.assertRaises(RuleError):
            c.isAce
            c.isFacecard
            c.rank
            c.name
            c.suit
            c.softValue
            c.hardValue

    def test_equality(self):
        c1 = Card('ace', 'spades')
        c2 = Card('ace', 'spades')
        c3 = Card('king', 'hearts')
        c4 = Card('queen', 'spades')

        c1.flip()
        c2.flip()
        c3.flip()
        c4.flip()

        self.assertTrue(c1 == c2, 'Identical cards should be equal.')
        self.assertFalse(c1 == c3, 'Cards with the same suit are not necessarily equal.')
        self.assertFalse(c3 == c4, 'Cards with the same value are not necessarily equal.')

        self.assertTrue(c1.same_rank(c2), 'two aces should have the same rank.')
        self.assertFalse(c1.same_rank(c3), 'Ace and king have different ranks.')
        self.assertFalse(c3.same_rank(c4), 'King and queen have different ranks.')

        self.assertTrue(c1.same_suit(c2), 'Identical cards have the same suit.')
        self.assertTrue(c1.same_suit(c4), 'Two spades should have the same suit.')
        self.assertFalse(c1.same_suit(c3), 'Spades and hearts should not be equal')


if __name__ == '__main__':
    unittest.main(verbosity=2)

class SchopskopfCard(Card):

    def __eq__(self, other):
        return self.suit == other.suit and self.name == other.name
