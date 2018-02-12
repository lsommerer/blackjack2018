from random import randint
from deck import Deck
from cardcollection import CardCollection
from toolbox import is_integer


class Shoe(CardCollection):

    def __init__(self, decks = 6):
        super().__init__()
        if not is_integer(decks):
            raise TypeError('Number of decks must be an integer.')
        for _ in range(decks):
            for card in Deck():
                self.append(card)
        self.set_cut_card()

    def set_cut_card(self):
        """
        Cut Card is the number of cards that should be left in the shoe. If
        the number of cards in the shoe falls below this number, the shoe
        needs to be shuffled. We set it at 40 (a reasonable minimum number
        of cards you might need to play blackjack with 7 people) plus upto
        25% of the size of the shoe.
        """
        minShoeLength = 40
        self.cutCard = minShoeLength + randint(int(0.25 * len(self)))

    def should_shuffle(self):
        """
        This method is called by the dealer before each game. It
        returns true if there are fewer cards left in the shoe than
        the position of the 'cut card' position which is determined
        when the shoe is shuffled."""
        return len(self) < self.cutCard

    def shuffle(self):
        super().shuffle()
        self.set_cut_card()



