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

class GlinesBotThree(Player):
    """
    This bot always bets one tenth of his money, doubles on all 9, 10 & 11
    never splits and hits the same as a dealer.
    """

    def __init__(self, money):
        super().__init__('GlinesBot 3', money)

    def bet_or_leave(self):
        if self.money >= 5:
            bet = 5
            if bet < 1:
                bet = 1
        else:
            bet = self.money
        return bet

    def wants_insurance(self):
       return False

    def play(self, hand, dealerShowing):
        additionalBet = None
        canSplit = False
        ace = False
        if hand[0].name == 'ace' or hand[1].name == 'ace':
            ace = True
        if hand[0].name == hand[1].name and hand.can_split() == True and self.money >= hand.bet:
            canSplit = True
        if canSplit == True and hand[0].name == 'ace':
            choice = 'p'
        elif canSplit == True and hand[0].name == '8':
            choice = 'p'
        elif canSplit == True and hand[0].name in ['2', '3', '6', '7', '9'] and dealerShowing.name in ['2', '3', '4', '5', '6']:
            choice = 'p'
        elif hand.can_double() and self.money >= hand.bet and hand.value() in [9, 10, 11]:
            if dealerShowing.name in ['2', '3', '4', '5', '6']:
                choice = 'd'
                additionalBet = hand.bet
            else:
                choice = 'h'
        # elif ace == True:
        #     print('hello')
        #     if hand.soft_value() in [13, 14, 15]:
        #         print('hello1')
        #         choice = 'h'
        #     elif hand.soft_value() in [16, 17, 18]:
        #         print('hello2')
        #         if dealerShowing.name in ['2', '3', '4', '5', '6']:
        #             choice = 'd'
        #         else:
        #             choice = 'h'
        #     else:
        #         choice = 's'
        elif hand.hard_value() in [4, 5, 6, 7, 8, 12, 13, 14, 15, 16]:
            if dealerShowing.name in ['2', '3', '4', '5', '6']:
                choice = 's'
            else:
                choice = 'h'
        else:
            choice = 's'
        return choice, additionalBet

class TessaBot(Player):
    """
    Always bets 2 at start of round (if possible) and never wants insurance.
    Always doubles down on 10 & 11 if dealer not showing a 10 or 11.
    Player will split if double of 11s or 9s.
    Player will stand if hand >= 17.
    Player will stand if hand >= 12, and dealer showing < 7.
    """

    def __init__(self, money):
        super().__init__('Tessa', money)

    def bet_or_leave(self):
        if self.money >= 2:
            bet = 2
        else:
            bet = self.money

        return bet

    def wants_insurance(self):
        return False

    def play(self, hand, dealerShowing):
        additionalBet = None
        choice = 's'
        #
        # split conditions
        #
        if hand.can_split() and self.money >= hand.bet and (hand.value() == 18 or hand.value() == 22):
            choice = 'p'
        #
        # double down conditions
        #
        elif (hand.can_double() and
              self.money >= hand.bet and
              hand.value() in [10, 11] and
              dealerShowing.softValue != 10 and
              dealerShowing.softValue != 11):
            choice = 'd'
            additionalBet = hand.bet
        #
        # hit conditions
        #
        elif hand.value() < 17:
            if hand.value() >= 12 and dealerShowing.softValue >= 7:
                choice = 'h'
            elif hand.value() < 12:
                choice = 'h'



        return choice, additionalBet

class IanThree(Player):
    def __init__(self, money):
        super(IanThree, self).__init__('Hitler Did Nothing Wrong', money)

    def bet_or_leave(self):
        betMoney = self.money/2
        if betMoney < 10:
            bet = self.money
        elif betMoney < 500:
            bet = self.money/4
        else:
            bet = self.money/2
        return bet

    def wants_insurance(self):
        return False

    def play(self, hand, dealerShowing):
        if dealerShowing.hardValue > 15:
            play = 's'
        else:
            if hand.value() in [9, 10, 11, 12] and hand.can_double():
                if self.money > hand.bet/2:
                    play = 'd'
                else:
                    play = 'h'
            elif hand.value() > 17:
                play = 's'
            elif hand.value() == 17:
                plays = ['s', 'h']
                play = plays[randint(0, 1)]
            elif hand.can_split():
                if self.money < 250:
                    play = 's'
                else:
                    play = 'p'
            else:
                play = 'h'
        if play == 'd':
            if self.money > hand.bet:
                additionalBet = hand.bet/4
            elif self.money > hand.bet/2:
                additionalBet = hand.bet/2
            else:
                additionalBet = self.money/6
        else:
            additionalBet = None
        return play, additionalBet

class RichBot(Player):

    def __init__(self, money):
        super().__init__('RichBot', money)

    def bet_or_leave(self):
        if self.money >= 5:
            bet = 5
        #
        # IMPORTANT! Make sure you still have a bet, even if you have
        # less money left than your normal bet.
        #
        else:
            bet = self.money
        return bet

    def wants_insurance(self):
       return False

    def play(self, hand, dealerShowing):
        additionalBet = None
        #
        # IMPORTANT! You have to check that you have enough money to
        # to double down or to split.
        #
        if hand.can_split() and self.money >= hand.bet:
            split = False
            for card in hand:
                if card.isAce:
                    split = True
            if split:
                choice = 'p'
        elif hand.can_double() and self.money >= hand.bet:
            if hand.value() == 11:
                choice = 'd'
                additionalBet = hand.bet
        if dealerShowing.rank in ["10", "11"]:
            if hand.value() < 17:
                choice = 'h'
            else:
                choice = 's'
        elif dealerShowing.rank in ["5", "6"]:
            if hand.value() < 12:
                choice = 'h'
            else:
                choice = 's'
        elif dealerShowing.rank in ["7", "8"]:
            if hand.value() < 16:
                choice = 'h'
            else:
                choice = 's'
        else:
            if hand.value() < 14:
                choice = 'h'
            else:
                choice = 's'
        return choice, additionalBet

class StreichBotOne(Player):

    def __init__(self, money):
        super().__init__('Zac Streich', money)
        self.maxMoney = self.money

    def bet_or_leave(self):
        if self.money >= self.maxMoney * .2:
            bet = self.money * .025
        elif self.maxMoney >= self.maxMoney * .1 and self.money < self.maxMoney * .2:
            bet = self.money * .015
        elif self.money > 0 and self.money < self.maxMoney * .1:
            bet = self.money
        else:
            bet = -1
        return bet

    def bet_or_leave1(self):
        if self.money >= 5:
            bet = 5
        else:
            bet = self.money
        return bet


    def wants_insurance(self):
       return False

    def play1(self, hand, dealerShowing):
        additionalBet = None
        if hand.can_double() and self.money >= hand.bet and hand.value() in [9, 10, 11] and dealerShowing.softValue  < 8:
            choice = 'd'
            additionalBet = hand.bet
        elif hand.can_split() == True:
            choice = "s"
        elif hand.value() <= 17:
            choice = "h"
        else:
            choice = 's'
        return choice, additionalBet

    def play(self, hand, dealerShowing):
        additionalBet = None
        #print(hand)
        #print(dealerShowing)
        if hand.value() in [9,10,11]:
            #print("First")
            if dealerShowing.softValue <= 5 and self.money >= hand.bet and hand.can_double():
                choice = "d"
                additionalBet = hand.bet
            else:
                if hand.can_hit():
                    choice = "h"
        elif hand.value() <= 8 and hand.value() > 2:
            #print("Second")
            if hand.can_split() and dealerShowing.softValue <= 9 and self.money >= hand.bet:
                choice = "p"
            else:
                choice = "h"
        elif hand.value() in [12,13,14,15]:
            #print("Third")
            if dealerShowing.softValue >= 8:
                choice = "h"
            else:
                choice = "s"
        elif hand.value() == 16:
            #print("Forth")
            if self.money >= hand.bet and hand.can_split():
                choice = "p"
            else:
                if dealerShowing.softValue >= 9:
                    choice = "h"
                else:
                    choice = "s"
        elif hand.value() == 17:
            #print("Fifth")
            if dealerShowing.softValue >= 10:
                choice = "h"
            else:
                choice = "s"
        elif hand.value() > 17:
            #print("Sixth")
            choice = "s"
        elif hand.value() == 2:
            #print("Seventh")
            if self.money >= hand.bet:
                choice = "p"
            else:
                choice = "h"
        else:
            #print("Else Statement")
            choice = "s"
        return choice, additionalBet

class BadRachelBot(Player):

    def __init__(self, money):
        super().__init__('badRachelBot', money)

    def bet_or_leave(self):
        if self._chips > 10:
            bet = randint(5, int(self._chips / 2))
        else:
            bet = -1
        return bet

    def wants_insurance(self):
        return False

    def play(self, hand, dealerShowing):

        additionalBet = None

        if hand.can_split() and self._chips >= hand.bet:
            choice = 'p'
        else:
            if hand.value() < 14:
                choice = 'h'
            else:
                choice = 's'

        return choice, additionalBet

class BadRachelBot2(Player):

    def __init__(self, money):
        super().__init__('badRachelBot2', money)

    def bet_or_leave(self):
        if self.money >= 10:
            bet = randint(1,6)
        elif self.money > 5:
            bet = 5
        else:
            bet = self.money
        return bet

    def wants_insurance(self):
        return False

    def play(self, hand, dealerShowing):

        additionalBet = None

        if hand.can_split() and hand[0].softValue >= 10 and self.money >= hand.bet:
            choice = 'p'
        elif hand.can_double() and hand.soft_value() == 11 and self.money >= hand.bet and dealerShowing.softValue != 11:
            choice = 'd'
            additionalBet = hand.bet
        elif dealerShowing.softValue == 5 or dealerShowing.softValue == 6 and hand.soft_value() >= 14:
            choice = 's'
        else:
            if hand.value() < 15:
                choice = 'h'
            else:
                choice = 's'

        return choice, additionalBet


######################################################
#
# BASIC BLACKJACK STRATEGY PLAYER CLASS
#
######################################################
class SommererBotBasicStrategy(Player):

    S = 0  # [S]tand
    H = 1  # [H]it
    D = 2  # [D]ouble down
    P = 3  # s[P]lit
    U = 4  # s[U]rrender (not currently implemented, so treat as a hit)

    decisions = ['S', 'H', 'D', 'P', 'U']

    # Dealer's card:    2, 3, 4, 5, 6, 7, 8, 9, T, A     hard value of your hand:
    hardValueMatrix = [[H, H, H, H, H, H, H, H, H, H],  # 2 (only if we just split <2,2>
                       [H, H, H, H, H, H, H, H, H, H],  # 3 (don't think this one is possible)
                       [H, H, H, H, H, H, H, H, H, H],  # 4
                       [H, H, H, H, H, H, H, H, H, H],  # 5
                       [H, H, H, H, H, H, H, H, H, H],  # 6
                       [H, H, H, H, H, H, H, H, H, H],  # 7
                       [H, H, H, H, H, H, H, H, H, H],  # 8
                       [H, D, D, D, D, H, H, H, H, H],  # 9
                       [D, D, D, D, D, D, D, D, H, H],  # 10
                       [D, D, D, D, D, D, D, D, D, H],  # 11
                       [H, H, S, S, S, H, H, H, H, H],  # 12
                       [S, S, S, S, S, H, H, H, H, H],  # 13
                       [S, S, S, S, S, H, H, H, H, H],  # 14
                       [S, S, S, S, S, H, H, H, U, H],  # 15
                       [S, S, S, S, S, H, H, U, U, U],  # 16
                       [S, S, S, S, S, S, S, S, S, S],  # 17 Always Stand
                       [S, S, S, S, S, S, S, S, S, S],  # 18 Always Stand
                       [S, S, S, S, S, S, S, S, S, S],  # 19 Always Stand
                       [S, S, S, S, S, S, S, S, S, S],  # 20 Always Stand
                       [S, S, S, S, S, S, S, S, S, S]]  # 21 Always Stand

    # Dealer's card:    2, 3, 4, 5, 6, 7, 8, 9, T, A     soft value of your hand:
    softValueMatrix = [[P, P, P, P, P, P, P, P, P, P],  # 12 <A,A> (2 aces always split)
                       [H, H, H, D, D, H, H, H, H, H],  # 13 <A,2> (or <A,A,A> and so forth)
                       [H, H, H, D, D, H, H, H, H, H],  # 14 <A,3>
                       [H, H, D, D, D, H, H, H, H, H],  # 15 <A,4>
                       [H, H, D, D, D, H, H, H, H, H],  # 16 <A,5>
                       [H, D, D, D, D, H, H, H, H, H],  # 17 <A,6>
                       [S, D, D, D, D, S, S, H, H, H],  # 18 <A,7>
                       [S, S, S, S, S, S, S, S, S, S],  # 19 <A,8>
                       [S, S, S, S, S, S, S, S, S, S],  # 20 <A,9>
                       [S, S, S, S, S, S, S, S, S, S]]  # 21 <A,10> (blackjack!)

    # Dealer's card:    2, 3, 4, 5, 6, 7, 8, 9, T, A     contents of your hand:
    pairValueMatrix = [[P, P, P, P, P, P, P, P, P, P],  # <A,A>  (always split aces)
                       [P, P, P, P, P, P, H, H, H, H],  # <2,2>
                       [P, P, P, P, P, P, H, H, H, H],  # <3,3>
                       [H, H, H, P, P, H, H, H, H, H],  # <4,4>
                       [D, D, D, D, D, D, D, D, H, H],  # <5,5>
                       [P, P, P, P, P, H, H, H, H, H],  # <6,6>
                       [P, P, P, P, P, P, H, H, H, H],  # <7,7>
                       [P, P, P, P, P, P, P, P, P, P],  # <8,8>
                       [S, P, P, P, P, S, P, P, S, S],  # <9,9>
                       [S, S, S, S, S, S, S, S, S, S]]  # <10,10> (never split 10s)

    def __init__(self, money):
        super().__init__('Sommerer 4', money)


    def play(self, hand, dealerShowing):
        """Use basic strategy to decide what to do."""
        #
        # Decide which of the three matrix apply, and
        # which row in the matrix to use.
        #
        if hand.can_split():
            matrix = SommererBotBasicStrategy.pairValueMatrix
            row =  hand[0].hardValue - 1
        elif hand.hard_value() <= 21:
            matrix = SommererBotBasicStrategy.hardValueMatrix
            row = hand.hard_value() - 2
        else:
            matrix = SommererBotBasicStrategy.softValueMatrix
            row = hand.soft_value() - 12
        #
        # Choose the column based on the dealer's card and
        # then choose the letter
        #
        try:
            column = dealerShowing.softValue - 2
            decisionNumber = matrix[row][column]
            decisionLetter = SommererBotBasicStrategy.decisions[decisionNumber]
        except:
            print('row: ', row)
            print('column: ', column)
            print('dealer: ', dealerShowing)
            print('player: ', hand)
            print('matrix:')
            for row in matrix:
                print(row)
            raise
        #
        # Surrender isn't implemented
        #
        if decisionLetter == 'U':
            decisionLetter = 'H'
        #
        # If you are splitting or doubling down, make sure you have enough money.
        #
        if decisionLetter in 'DP' and self.money <= hand.bet:
            decisionLetter = 'H'
        additionalBet = hand.bet
        #print(decisionLetter, self)
        return decisionLetter, additionalBet

    def bet_or_leave(self):
        """
        At the start of each round the player can either bet by entering an amount
        to bet, sit this hand out by entering 0 for a bet, or leave the table by
        entering -1.
        """
        if self.money >= 2:
            bet = 2
        else:
            bet = self.money
        return bet

    def wants_insurance(self):
        """
        Returns True if the player should buy insurance else return False.

        This procedure is called by the dealer after all players have bet and
        receives their cards and after the dealer has received his cards. It is
        only called if the dealer is showing an ace (the dealer might have blackjack).
        """
        return False

