from player import Player

class SommererBotOne(Player):
    """
    This bot will always split, double down and buy insurance. It plays it's hand like
    the dealer.
    """

    def __init__(self, money):
        super().__init__('Sommerer 1', money)

    def bet_or_leave(self):
        if self.money >= 2:
            bet = 2
        else:
            bet = self.money
        return bet

    def wants_insurance(self):
       return True

    def play(self, hand, dealerShowing):
        additionalBet = None
        if hand.can_split() and self.money >= hand.bet:
            choice = 'p'
        elif hand.can_double() and self.money >= hand.bet:
            choice = 'd'
            additionalBet = hand.bet
        elif hand.value() < 17:
            choice = 'h' #hit
        else:
            choice = 's' #stand
        return choice, additionalBet

class SommererBotTwo(Player):
    """
    This bot really hates to bust and will never hit on anything higher than an 11.
    """

    def __init__(self, money):
        super().__init__('Sommerer 2', money)

    def bet_or_leave(self):
        if self.money >= 4:
            bet = 4
        else:
            bet = self.money
        return bet

    def wants_insurance(self):
       return False

    def play(self, hand, dealerShowing):
        additionalBet = None
        if hand.value() < 12:
            choice = 'h' #hit
        else:
            choice = 's' #stand
        return choice, additionalBet

class SommererBotThree(Player):
    """
    This bot really hates to bust and will never hit on anything higher than an 11.
    """

    def __init__(self, money):
        super().__init__('Sommerer 3', money)

    def bet_or_leave(self):
        if self.money >= 1:
            bet = self.money/10
            if bet < 1:
                bet = 1
        else:
            bet = self.money
        return bet

    def wants_insurance(self):
       return False

    def play(self, hand, dealerShowing):
        additionalBet = None
        if hand.can_double() and self.money >= hand.bet and hand.value in [9, 10, 110]:
            choice = 'd'
            additionalBet = hand.bet
        elif hand.value() < 17:
            choice = 'h' #hit
        else:
            choice = 's' #stand
        return choice, additionalBet
