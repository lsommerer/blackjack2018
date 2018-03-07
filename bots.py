from player import Player
from random import *

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
        super().__init__('Tessa', money=100)

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

    def __init__(self, money=1000):
        super().__init__(name='badRachelBot')

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
