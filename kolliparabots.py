from player import Player
from random import *
from hand import Hand
from card import Card

class Ian(Player):
    def __init__(self, money=1000):
        super(Ian, self).__init__( name='Ian Bot 1000')

    def bet_or_leave(self):
        if self.money < 500:
            options = ['bet', 'leave']
            choice = options[randint(0,1)]
        else:
            choice = 'bet'
        if choice == 'bet':
            bet = randint(0,int(self.money))
        elif choice == 'leave':
            bet = -1
        return bet

    def wants_insurance(self):
        choice = randint(0,1)
        if choice == 1:
            return True
        else:
            return False

    def play(self, hand, dealerShowing):
        plays = ['s','p','d','h']
        if not hand.can_split() or self.money < hand.bet:
            plays.remove('p')
        if not hand.can_double() or self.money < hand.bet:
            plays.remove('d')
        choice = plays[randint(0,len(plays)-1)]
        if choice == 'd':
            additionalBet = randint(0,hand.bet)
        else:
            additionalBet = 0
        return choice, additionalBet