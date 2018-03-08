from player import Player
from random import *
from time import sleep

class SommererBotOne(Player):
    """
    This bot will always split, double down and buy insurance. It hits on anything less than
    17 like the dealer, but that doesn't happen very often since he is
    always doubling down. He always bets $2.00.
    """

    def __init__(self, money):
        super().__init__('Sommerer 1', money)

    def bet_or_leave(self):
        if self.money >= 2:
            bet = 2
        #
        # IMPORTANT! Make sure you still have a bet, even if you have
        # less money left than your normmal bet.
        #
        else:
            bet = self.money
        return bet

    def wants_insurance(self):
       return True

    def play(self, hand, dealerShowing):
        additionalBet = None
        #
        # IMPORTANT! You have to check that you have enough money to
        # to double down or to split.
        #
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
    Better safe than sorry.
    """

    def __init__(self, money):
        super().__init__('Sommerer 2', money)

    def bet_or_leave(self):
        if self.money >= 4:
            bet = 4
        #
        # IMPORTANT! Make sure you still have a bet, even if you have
        # less money left than your normmal bet.
        #
        else:
            bet = self.money
        return bet

    def wants_insurance(self):
        insurance = False
        #
        # IMPORTANT! If you want insurance, make sure you check that you
        # have enough money for it.
        #
        if self.money > self.hands[0].bet:
            insurance = True
        return insurance

    def play(self, hand, dealerShowing):
        additionalBet = None
        if hand.value() < 12:
            choice = 'h' #hit
        else:
            choice = 's' #stand
        return choice, additionalBet

class SommererBotThree(Player):
    """
    This bot always bets one tenth of his money, doubles on all 9, 10 & 11
    never splits and hits the same as a dealer.
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
        if hand.can_double() and self.money >= hand.bet and hand.value() in [9, 10, 11]:
            choice = 'd'
            additionalBet = hand.bet
        elif hand.value() < 17:
            choice = 'h' #hit
        else:
            choice = 's' #stand
        return choice, additionalBet
