from random import randint
from deck import Deck
from cardcollection import CardCollection
from toolbox import is_integer


class Shoe(CardCollection):

    def __init__(self, decks = 6):
        super().__init__()
        if not is_integer(decks):
            raise TypeError('Number of decks must be an integer.')
        self.__decks = decks
        self.populate_shoe()
        self.set_cut_card()

    def populate_shoe(self):
        """Adds the specified number of decks of cards to the shoe."""
        self.clear()
        for _ in range(self.__decks):
            for card in Deck():
                self.append(card)

    def set_cut_card(self):
        """
        Cut Card is the number of cards that should be left in the shoe. If
        the number of cards in the shoe falls below this number, the shoe
        needs to be shuffled. We set it at 40 (a reasonable minimum number
        of cards you might need to play blackjack with 7 people) plus upto
        20% of the size of the shoe.
        """
        minShoeLength = 40
        maxPercentLeft = 0.20
        self.cutCard = minShoeLength + randint(0, int(maxPercentLeft* len(self)))

    def should_shuffle(self):
        """
        This method is called by the dealer before each round. It
        returns true if there are fewer cards left in the shoe than
        the position of the 'cut card' position. The cut card
        position is determined when the shoe is shuffled.
        """
        return len(self) <= self.cutCard

    def shuffle(self):
        """
        Cards may have been delt from the shoe, so make sure we have a complete
        shoe before we shuffle it.
        """
        self.populate_shoe()
        super().shuffle()
        self.set_cut_card()

# [ ] 1. create a new shoe
# [ ] 2. print the shoe
# [ ] 3. shuffle the shoe
# [ ] 4. print the shoe
# [ ] 5. create a shoe with 2 decks
# [ ] 6. create a shoe with 1 deck
# [ ] 7. fail gracefully to create a shoe with 0.5 decks
# [ ] 8. create a shoe with 1 deck
# [ ] 9. print the shoe
# [ ] 10. draw a card from the shoe
# [ ] 11. print the card (was it correct)
# [ ] 12. draw 10 cards from the shoe
# [ ] 13. print the shoe
# [ ] 14. draw cards until you are past the cut card
# [ ] 15. shuffle the shoe
# [ ] 16. print the shoe
# [ ] 17. draw 40 cards from the shoe

