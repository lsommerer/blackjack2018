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

    useUnicode = True
    totalCards = 0

    def __init__(self, name, suit):
        #
        # Check that the name is legal
        #
        if name.lower() in Card.names:
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
        self.__showing = False
        self.__hardValue = Card.hardValueDict[self.__name]
        self.__softValue = Card.softValueDict[self.__name]
        Card.totalCards += 1

    def __str__(self):
        if Card.useUnicode:
            suitString = Card.unicodeDict[self.__suit]
        else:
            suitString = self.__suit.capitalize()
        #        return "%s of %s" % (nameString,suitString)
        return "%s%s" % (self.__shortName, suitString)

    def __repr__(self):
        return "Card('%s','%s')" % (self.__name, self.__suit)

    def __eq__(self, other):
        equal = False
        if self.__softValue == other.__softValue:
            equal = True
        return equal

    def is_showing(self):
        """Returns True if the card is face-up and can be seen."""
        return self.__showing

    def is_facecard(self):
        """Returns True if the card is a facecard."""
        if not self.is_showing():
            raise RuleError('card is not showing, you can not use is_face_card()')
        return self.__isFacecard

    def is_ace(self):
        """Returns True if the card is an ace."""
        if not self.is_showing():
            raise RuleError('card is not showing, you can not use is_ace()')
        return self.__isAce

    def hard_value(self):
        """Returns the hard value of the card."""
        if not self.is_showing():
            raise RuleError('card is not showing, you can not use hard_value()')
        return self.__hardValue

    def soft_value(self):
        """Returns the soft value of the card."""
        if not self.is_showing():
            raise RuleError('card is not showing, you can not use hard_value()')
        return self.__softValue

    def flip(self):
        """Flips the card over from 'showing' to 'not showing' or visa versa."""
        self.__showing = not self.__showing

    def suit(self):
        """Returns the suit of the card."""
        if not self.is_showing():
            raise RuleError('card is not showing, you can not use suit()')
        return self.__suit

    def name(self):
        """Returns the name of the card."""
        if not self.is_showing():
            raise RuleError('card is not showing, you can not use name()')
        return self.__name
