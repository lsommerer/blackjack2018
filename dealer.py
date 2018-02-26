from player import Player
from hand import Hand
from shoe import Shoe
from toolbox import is_number
from table import Table

class Dealer(Player):

    def __init__(self):
        super(self).__init__()
        self._playingPlayers = []
        self._playersWithInsurance = []
        self._shoe = Shoe()

    def sit(self, table):
        """Override the player sit method. so that the dealer sits on the right side of the table."""
        if type(table) == Table:
            self._table = table
            table.add_dealer(self)
        else:
            raise TypeError('Table parameter must be of type Table.')

    def bet_or_leave(self):
        """
        At the start of each round the player can either bet by entering an amount
        to bet, sit this hand out by entering 0 for a bet, or leave the table by
        entering -1.
        """
        #
        # The dealer will not be in the list of players, so this method will not be
        # called on the dealer.
        #
        pass

    def want_insurance(self):
        """
        Returns True if the player should buy insurance else return False.

        This procedure is called by the dealer after all players have bet and
        receives their cards and after the dealer has received his cards. It is
        only called if the dealer is showing an ace (the dealer might have blackjack).
        """
        #
        # The dealer will not be in the list of players, so this method will not be
        # called on the dealer.
        #
        pass

    def play(self, hand, dealerShowing):
        """
        Returns the player's action for this hand. The dealer calls this method
        repeatedly for each of the player's hands until all hands are completed.
        Valid return values are listed below. Note that two values are returned:

        choice: one of the plays listeded below
        additionalBet: the amount to "double down" by

        additionalBet is discarded by the caller in all other cases.

        allPlays = {'s': '[S]tand',
                    'h': '[H]it',
                    'd': '[D]ouble down',
                    'p': 's[P]lit',
                    'u': 's[U]rrender'}
        return choice, additionalBet
        """
        if hand.value < 17:
            choice = 'h' #hit
        else:
            choice = 's' #stand
        additionalBet = None
        return choice, additionalBet

    def take_bets(self):
        self._playingPlayers = []
        leavingPlayers = []
        for player in self._table.players:
            # = -1: player is leaving the table
            # =  0: players is sitting this hand out
            # >  0: player is betting this amount
            betAmount = player.bet_or_leave()
            name = player.name.capitalize()
            if betAmount == -1:  # leaving table
                leavingPlayers.append(player)
                print(f"{name} is leaving the table with ${player.money:0.2f}.")
            elif betAmount == 0:
                print(f"{name} is sitting this hand out.")
            elif betAmount > 0 and player.money > betAmount:
                self._playingPlayers.append(player)
                player.rake_out(betAmount)
                self.rake_in(betAmount)
                player.add_hand(Hand(betAmount))
                print(f"{name} is betting ${betAmount:0.2f}.")
            else:
                print(f"{name} doesn't have enough money to bet ${betAmount:0.2f}. Sitting this hand out.")
            for player in leavingPlayers:
                self._table.leave_table(player)


    def deal(self):
        """
        Deal an initial 2 cards to each player and to the dealer.
        """
        #
        # Shuffle the cards if we need to.
        #
        if self._shoe.should_shuffle():
            self._shoe.shuffle()
        #
        # Deal cards to each player.
        #
        cardsToDeal = 2
        for _ in range(cardsToDeal):
            for player in self._playingPlayers:
                card = self._shoe.draw()
                card.flip()
                player.hands[0].hit(card)
        #
        # Deal yourself some cards.
        #
        self.add_hand(Hand(0))
        self.hands[0].hit(self._shoe.draw().flip())
        self.hands[0].hit(self._shoe.draw())

    def offer_insurance(self):
        self._playersWithInsurance = []
        if self.hands[0][1].name == 'ace':
            for player in self._playingPlayers:
                if player.wants_insurance():
                    self._playersWithInsurance.append(player)

    def play_hands(self):
        dealerShowing = self.hands[0][1]
        for player in self._playingPlayers:
            for hand in player.hands:
                while hand.can_hit():
                    playerDecision, additionalBet = player.play(hand,dealerShowing)
                    #
                    # [S]tand
                    #
                    if playerDecision == 's':
                        hand.stand()
                    #
                    # [H]it
                    #
                    elif playerDecision == 'h':
                        hand.hit(self._shoe.draw().flip())
                    #
                    # s[P]lit
                    #
                    elif playerDecision == 'p':
                        if hand.can_split() and player.money >= hand.bet:
                            self.rake_in(player.rake_out(hand.bet))
                            newHand = Hand(hand.bet).hit(hand.split())
                            newHand.hit(self._shoe.draw().flip())
                            player.add_hand(newHand)
                            hand.hit(self._shoe.draw().flip())
                        else:
                            print("Sorry, you can't split this hand (pick again).")
                    #
                    # [D]ouble down
                    #
                    elif playerDecision == 'd':
                        if hand.can_double() and is_number(additionalBet) and player.money >= additionalBet:
                            hand.double_down(self._shoe.draw().flip(), additionalBet)
                            self.rake_in(player.rake_out(additionalBet))
                        else:
                            print("Sorry, you can't double this hand (pick again).")
                    #
                    # s[U]rrender
                    #
                    elif playerDecision == 'u':
                        print('Sorry, surrender is not implemented (pick again).')
                    #
                    # [A]nything else
                    #
                    else:
                        print(f"I'm sorry, I don't know what '{playerDecision}' means.")

    def play_own_hand(self):
        playingPlayers = self._playingPlayers
        self._playingPlayers = [self]
        self.play_hands()
        self._playingPlayers = playingPlayers

    def payout_hands(self):
        dealerHand = self.hands[0]
        for player in self._playingPlayers:
            for hand in player:
                if hand.isBusted:
                    pass
                elif hand.isBlackJack and not dealerHand.isBlackJack:
                    pass
                elif hand.isBlackJack and dealerHand.isBlackJack:
                    pass
                elif hand == dealerHand:
                    pass
                elif dealerHand.isBusted:
                    pass
                elif hand > dealerHand:
                    pass
        for player in self._playersWithInsurance:
            if dealerHand.isBlackJack:
                pass



