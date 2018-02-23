from card import Card
from random import randrange


class CardCollection(list):

    def __init__(self):
        super().__init__(self)

    def __str__(self):
        if len(self) == 0:
            string = '[no cards]'
        else:
            debugMode = Card.debugMode
            Card.debugMode = True
            string = '['
            for card in self:
                string += str(card) + ', '
            string = string[:-2] + "]"
            Card.debugMode = debugMode
        return string

    def shuffle(self):
        """Shuffles the collection in place"""
        for pos1 in range(len(self)):
            pos2 = randrange(len(self))
            self[pos1], self[pos2] = self[pos2], self[pos1]

    def draw(self):
        """Returns the top card from the collection; removing it from the deck in the process."""
        if len(self) > 0:
                card = self.pop()
        else:
            raise ValueError('Not enough cards left to draw one.')
        return card

    def flip(self):
        """Turn over all the cards in the collection. Useful for testing."""
        for card in self:
            card.flip()
