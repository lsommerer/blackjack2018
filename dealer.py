from player import Player
from hand import Hand
from shoe import Shoe
from toolbox import is_number
from table import Table
from time import sleep

class Dealer(Player):

    def __init__(self, name = 'Bob the dealer', money = 1000000, delay = 1, verbose = True):
        super().__init__(name, money)
        self._playingPlayers = []
        self._playersWithInsurance = []
        self._shoe = Shoe()
        self.delay = delay
        self.isVerbose = verbose

    def sit(self, table):
        """Override the player sit method. so that the dealer sits on the right side of the table."""
        self._table = table
        table.add_dealer(self)

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

    def wants_insurance(self):
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
        if hand.value() < 17:
            choice = 'h' #hit
        else:
            choice = 's' #stand
        additionalBet = None
        return choice, additionalBet


    def switch_shoe(self, shoe):
        """
        When we run a simulation instead of a game, we want to make sure that all of
        dealers are using the same shoe and switching shoes at the same time.

        :param shoe: a preshuffled shoe, ready to be delt from.
        :type shoe: Shoe
        :return:
        """
        self._shoe = shoe
        for player in self._table.players:
            player.reset_count()


    def take_bets(self):
        sleep(self.delay)
        if self.isVerbose: print('\n---betting---')
        self._playingPlayers = []
        leavingPlayers = []
        for player in self._table.players:
            #
            # = -1: player is leaving the table
            # =  0: players is sitting this hand out
            # >  0: player is betting this amount
            #
            if self.isVerbose: print(f'\n{player}')
            betAmount = player.bet_or_leave()
            name = player.name.capitalize()
            if betAmount == -1 or player.money < 1:  # leaving table
                leavingPlayers.append(player)
                if self.isVerbose: print(f"{name} is leaving the table with ${player.money:0.2f}.")
            elif betAmount == 0:
                if self.isVerbose: print(f"{name} is sitting this hand out.")
            elif betAmount > 0 and player.money >= betAmount:
                self._playingPlayers.append(player)
                player.rake_out(betAmount)
                self.rake_in(betAmount)
                player.add_hand(Hand(betAmount))
                player.handsPlayed += 1
                player.totalWagers += betAmount
                if self.isVerbose: print(f"{name} is betting ${betAmount:0.2f}.")
            else:
                if self.isVerbose: print(f"{name} doesn't have enough money to bet ${betAmount:0.2f}. Sitting this hand out.")
            for player in leavingPlayers:
                self._table.leave_table(player)


    def show_card_to_players(self, card):
        """
        Make sure that players who might be counting cards get to see
        every card that is delt, not just the ones in their hands.
        """
        for player in self._playingPlayers:
            player.count(card)


    def deal(self):
        """
        Deal an initial 2 cards to each player and to the dealer.
        """
        #
        # Shuffle the cards if we need to.
        #
        if self._shoe.should_shuffle():
            self._shoe.shuffle()
            for player in self._table.players:
                player.reset_count()
            self._table.shuffling_shoe()
        #
        # Deal cards to each player.
        #
        cardsToDeal = 2
        for _ in range(cardsToDeal):
            for player in self._playingPlayers:
                card = self._shoe.draw().flip()
                player.hands[0].hit(card)
                self.show_card_to_players(card)
        #
        # Deal yourself some cards.
        #
        bet = 0
        self.add_hand(Hand(bet))
        card = self._shoe.draw().flip()
        #TODO remove this debugging code
#        print('shoe:', self._shoe)
#        print('draw test:', self._shoe.draw())
#        print('flip test:', self._shoe.draw().flip())
#        print('card:', card)
        self.hands[0].hit(card)
        self.show_card_to_players(card)
        self.hands[0].hit(self._shoe.draw().flip())


    def offer_insurance(self):
        print('\n')
        self._playersWithInsurance = []
        if self.hands[0][1].name == 'ace':
            for player in self._playingPlayers:
                if player.wants_insurance():
                    self._playersWithInsurance.append(player)
                    player.insurance = player.hands[0].bet/2
                    player.timesInsurance += 1

    def play_hands(self):
        """
        Loop through the players and let them choose what they want to do. Then
        process that decision.
        """
        playerOptions = {'s': self.player_stand,
                         'h': self.player_hit,
                         'p': self.player_split,
                         'd': self.player_double_down,
                         'u': self.player_surrender
                         }
        if self.isVerbose: print('\n---players are playing---')
        dealerShowing = self.hands[0][1]
        for player in self._playingPlayers:
            for hand in player.hands:
                if hand.isBlackJack:
                    if self.isVerbose: print(f"{player.name} has Blackjack! {hand}.")
                while hand.can_hit():
                    sleep(self.delay)
                    playerDecision, additionalBet = player.play(hand,dealerShowing)
                    if playerDecision in playerOptions:
                        which_option = playerOptions[playerDecision]
                        which_option(player, hand, additionalBet)
                    else:
                        if self.isVerbose: print(f"I'm sorry, I don't know what '{playerDecision}' means.")

    def player_stand(self, player, hand, *args):
        hand.stand()
        if self.isVerbose: print(f"{player.name} stands with {hand}.")

    def player_hit(self, player, hand, *args):
        card = self._shoe.draw().flip()
        self.show_card_to_players(card)
        hand.hit(card)
        if self.isVerbose: print(f"{player.name} hit and received a {card} {hand}.")
        player.timesHit += 1

    def player_split(self, player, hand, *args):
        if hand.can_split() and player.money >= hand.bet:
            self.rake_in(player.rake_out(hand.bet))
            newHand = Hand(hand.bet)
            newHand.hit(hand.split())
            card = self._shoe.draw().flip()
            self.show_card_to_players(card)
            newHand.hit(card)
            player.add_hand(newHand)
            card = self._shoe.draw().flip()
            self.show_card_to_players(card)
            hand.hit(card)
            if self.isVerbose: print(f"{player.name} split and now has: \n   {hand}\n   {newHand}")
            player.timesSplit += 1
            player.handsPlayed += 1
            player.totalWagers += hand.bet
        else:
            if self.isVerbose: print("Sorry, you can't split this hand (pick again).")

    def player_double_down(self, player, hand, additionalBet):
        if hand.can_double() and is_number(additionalBet) and player.money >= additionalBet:
            card = self._shoe.draw().flip()
            self.show_card_to_players(card)
            hand.double_down(card, additionalBet)
            self.rake_in(player.rake_out(additionalBet))
            if self.isVerbose: print(f"{player.name} doubled down and received a {card} {hand}.")
            player.timesDoubled += 1
            player.totalWagers += additionalBet
        else:
            if self.isVerbose: print("Sorry, you can't double this hand (pick again).")

    def player_surrender(self, player, hand, *args):
        print('Sorry, surrender is not implemented (pick again).')
        player.timesSurrendered += 1

    #TODO Make sure dealer shows hole card to players somewhere for counting.
    def play_own_hand(self):
        if self.isVerbose: print('\n---dealer is playing---')
        playerOptions = {'s': self.player_stand,
                         'h': self.player_hit}
        hand = self.hands[0]
        dealerShowing = hand[0]
        while hand.can_hit():
            playerDecision, additionalBet = self.play(hand,dealerShowing)
            which_option = playerOptions[playerDecision]
            which_option(self, hand, additionalBet)

    def payout_hands(self):
        if self.isVerbose: print('\n---results---')
        dealerHand = self.hands[0]
        for player in self._playingPlayers:
            sleep(self.delay * 2)
            for hand in player.hands:
                if hand.isBusted:
                    winnings = 0
                    text = 'lost'
                    player.timesBusted += 1
                    player.timesLost += 1
                elif hand.isBlackJack and not dealerHand.isBlackJack:
                    winnings = hand.bet * 2.5
                    text = 'won (Blackjack!)'
                    player.timesWon += 1
                    player.timesBlackjack += 1
                elif hand.isBlackJack and dealerHand.isBlackJack:
                    winnings = hand.bet
                    text = 'pushed (blackjack) and lost'
                    player.timesPushed += 1
                    player.timesBlackjack += 1
                elif not hand.isBlackJack and dealerHand.isBlackJack:
                    winnings = 0
                    text = 'lost'
                    player.timesLost += 1
                elif hand.value() == dealerHand.value():
                    winnings = hand.bet
                    text = 'pushed and lost'
                    player.timesPushed += 1
                elif dealerHand.isBusted:
                    winnings = hand.bet * 2
                    text = 'won (dealer busted)'
                    player.timesWon += 1
                elif hand.value() > dealerHand.value():
                    winnings = hand.bet * 2
                    text = 'won'
                elif hand.value() < dealerHand.value():
                    winnings = 0
                    text = 'lost'
                    player.timesLost += 1
                player.rake_in(winnings)
                self.rake_out(winnings)
                winnings = abs(winnings-hand.bet)
                if self.isVerbose: print(f"{player.name} {text} ${winnings:0.2f} on {hand}.")
        #
        # Payout any insurance bets.
        #
        for player in self._playersWithInsurance:
            if dealerHand.isBlackJack:
                winnings = player.insurance * 2
                player.rake_in(winnings)
                self.rake_out(winnings)
                if self.isVerbose: print(f"{player.name} won ${player.insurance:0.2f} on the insurance bet.")
            else:
                if self.isVerbose: print(f"{player.name} lost ${player.insurance:0.2f} on the insurance bet.")
        #
        # Clear the table and get ready for the next round.
        #
        for player in self._playingPlayers:
            player.discard_hands()
            player.insurance = 0
        self.discard_hands()
        if self.isVerbose: print('---results complete---')





