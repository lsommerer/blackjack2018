from player import Player
from random import *

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