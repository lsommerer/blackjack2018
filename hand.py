from errors import RuleError
from cardcollection import CardCollection


class Hand(CardCollection):

    def __init__(self, bet):
        if bet <= 0:
            raise ValueError('Bet must be greater than zero.')
        super().__init__()
        self.isVerbose = False
        self._bet = bet
        self._isBlackJack = False
        self._isBusted = False
        self._isStanding = False
        self._isSplit = False
        self._isDoubled = False

    def __str__(self):
        string = super().__str__()
        string += f" ({self.soft_value()},{self.hard_value()})"
        string += f" bet: ${self._bet:.2f}"
        if self._isBlackJack:
            string += " BlackJack!"
        if self._isSplit:
            string += " Split"
        if self._isDoubled:
            string += " Doubled"
        if self._isStanding:
            string += " Standing"
        elif self._isBusted:
            string += " Busted"
        else:
            string += " Playing"
        return string

    def __eq__(self, other):
        #
        # If they are both blackjack, then they are equal.
        #
        if self.isBlackJack and other.isBlackJack:
            equal = True
        #
        # If one is blackjack and the other is not, then they
        # are not equal.
        #
        elif self.isBlackJack != other.isBlackJack:
            equal = False
        #
        # Neither has a blackjack, so we can go by their value:
        #
        elif self.value() == other.value():
            equal = True
        else:
            equal = False
        return equal


    def hard_value(self):
        value = 0
        for card in self:
            value += card.hardValue
        return value

    def soft_value(self):
        numberOfAces = 0
        value = 0
        #TODO remove this debugging code
#        print('length of hand:',len(self))
#        print('hand:',self[0])
        for card in self:
            if card.isAce:
                numberOfAces += 1
            if numberOfAces > 1:
                value += card.hardValue
            else:
                value += card.softValue
        return value

    def value(self):
        value = self.soft_value()  # ace as 11
        if value > 21:
            value = self.hard_value()  # ace as 1
        return value

    def can_hit(self):
        canHit = True
        if self._isBlackJack or self._isDoubled or self._isBusted or self._isStanding:
            canHit = False
        return canHit

    def hit(self, card):
        if not self.can_hit():
            raise RuleError(f"Can't hit on this hand: {self}")
        if self.isVerbose:
            print("  hit and received: " + str(card))
        self.append(card)
        self.check_blackjack()
        self.check_21()
        self.check_busted()

    def stand(self):
        self._isStanding = True
        if self.isVerbose:
            print("  standing with: " + str(self))

    def can_split(self):
        canSplit = False
        if (len(self) == 2) and self[0].same_rank(self[1]) and not self._isStanding:
            canSplit = True
        return canSplit

    def split(self):
        """
        Causes the hand to split. Returns one of the cards in the hand so that
        that card can be used to form a new hand.
        """
        if not self.can_split():
            raise RuleError("Can't split this hand: " + str(self))
        if self.isVerbose:
            print("  splitting hand")
        self._isSplit = True
        card = self.pop()
        return card

    def can_double(self):
        """Anytime you can hit you can also double down."""
        return self.can_hit()

    def double_down(self, card, additionalBet = None):
        if additionalBet == None:
            additionalBet = self._bet
        if not self.can_double():
            raise RuleError("Can't double down on this hand: " + str(self))
        if additionalBet > self._bet:
            raise ValueError('Double Down bet can not be more than original bet.')
        if additionalBet <= 0:
            raise ValueError('Double Down bet can not be less than or equal to zero.')
        if self.isVerbose:
            print("  doubled down and received: " + str(card))
        self._bet += additionalBet
        self.hit(card)
        self._isDoubled = True
        self._isStanding = True

    def check_blackjack(self):
        if (self.value() == 21) and (len(self) == 2):
            self._isBlackJack = True
            self._isStanding = True
            if self.isVerbose:
                print("  Black Jack! Hand over.")

    def check_busted(self):
        if self.value() > 21:
            self._isBusted = True
            if self.isVerbose:
                print("  %s: busted! Hand over." % self.value())

    def check_21(self):
        if self.value() == 21:
            self._isStanding = True
            if self.isVerbose:
                print(f"  {self.value()}: I'm stanging.")

    def get_is_blackjack(self):
        return self._isBlackJack

    def get_is_busted(self):
        return self._isBusted

    def get_is_standing(self):
        return self._isStanding

    def get_is_split(self):
        return self._isSplit

    def get_is_doubled(self):
        return self._isDoubled

    def get_bet(self):
        return self._bet


    isBlackJack = property(get_is_blackjack)
    isBusted = property(get_is_busted)
    isStanding = property(get_is_standing)
    isSplit = property(get_is_split)
    isDoubled = property(get_is_doubled)
    bet = property(get_bet)

def informal_hand_test():
    from shoe import Shoe
    s = Shoe()
    h = Hand(10)
    h.isVerbose = True
    print(h)
    c = s.draw()
    c.flip()
    print(c)
    if h.can_hit():
        h.hit(c)
        print(h)
    c = s.draw()
    c.flip()
    print(c)
    if h.can_hit():
        h.hit(c)
        print(h)
    print('Can double:', h.can_double())
    print('Can hit:', h.can_hit())
    print('Can split:', h.can_split())
    c = s.draw()
    c.flip()
    h.double_down(c,h.bet)
    print(h)
    #should be busted now
    try:
        c = s.draw()
        c.flip()
        h.hit(c)
    except RuleError as error:
        print(error)
        print("tried and failed to hit a busted hand.")

if __name__ == '__main__':
    informal_hand_test()