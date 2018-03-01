from player import Player
from toolbox import get_string, get_boolean, get_number_between

class HumanPlayer(Player):

    def bet_or_leave(self):
        """
        At the start of each round the player can either bet by entering an amount
        to bet, sit this hand out by entering zero for a bet, or leave the table by
        entering -1.
        """
        prompt = f"{self.name}, enter your bet ('0' to sit out hand or '-1' to quit):"
        #TODO Fix this is pretty sketch way to get a valid input for bet amount.
        bet = -0.5
        while (bet > -1) and (bet < 0):
            bet = get_number_between(-1, self._chips, prompt)
        return bet


    def wants_insurance(self):
        """
        Returns True if the player should buy insurance else return False.

        This procedure is called by the dealer after all players have bet and
        receives their cards and after the dealer has received his cards. It is
        only called if the dealer is showing an ace (the dealer might have blackjack).
        """
        return get_boolean(f'{self.name}, do you want insurance? (The dealer has an ace showing)')


    def play(self, hand, dealerShowing):
        """
        Returns the player's action for this hand. The dealer calls this method
        repeatedly for each of the player's hands until all hands are completed.
        """
        allPlays = {'s': '[S]tand',
                    'h': '[H]it',
                    'd': '[D]ouble down',
                    'p': 's[P]lit',
                    'u': 's[U]rrender'}
        #
        # Some plays will not be legal for a given hand. Remove those choices.
        #
        if not hand.can_hit():
            del allPlays['h']
        if not hand.can_split() or (self._chips < hand.bet):
            del allPlays['p']
        if not hand.can_double() or (self._chips == 0):
            del allPlays['d']
        if hand.isStanding or hand.isBusted:
            del allPlays['s']
            del allPlays['u']

        assert len(allPlays) >0, "player.play() shouldn't be called if there are no legal plays."

        validPlays = allPlays.keys()
        print(f'\n{self.name} has {hand}.')
        print(f'The dealer has a {dealerShowing} showing.')
        validMenu = f'{self.name} can: ' + '   '.join(allPlays.values())

        choice = 'getInMyWhileLoop'
        while choice not in validPlays:
           choice = get_string(validMenu).lower()
        #
        # If the player doubles down, they can say by how much.
        #
        additionalBet = None
        if choice == 'd':
            maxBet = hand.bet
            if self._chips < maxBet:
                maxBet = self._chips
            prompt = f'{self.player}, how much do you want to bet? [max = ${maxBet:0.2f}]'
            additionalBet = get_number_between(0, maxBet, prompt)

        return choice, additionalBet


    def count(self, card):
        """This method will be called every time the dealer deals a card to anyone."""
        #
        # Use this if you want your player to count cards. The dealer will call this method
        # on the player and send it each card as the player would see them. You can create one
        # of more instance variables here for your other methods to access as needed.
        #
        pass


    def reset_count(self):
        """This method will be called for you every time the dealer shuffles the deck."""
        #
        # Use this if you are counting cards.
        #
        pass


def test():
    from card import Card
    from hand import Hand

    ace = Card('ace', 'spades')
    ten = Card('10', 'clubs')
    six = Card('6', 'hearts')
    five = Card('5', 'diamonds')

    ace.flip()
    ten.flip()
    six.flip()
    five.flip()

    blackjack = Hand(2)
    blackjack.hit(ace)
    blackjack.hit(ten)

    split = Hand(2)
    split.hit(ace)
    split.hit(ace)

    double = Hand(2)
    double.hit(six)
    double.hit(five)

    twentyone = Hand(2)
    twentyone.hit(ten)
    twentyone.hit(six)
    twentyone.hit(five)

    busted = Hand(2)
    busted.hit(ten)
    busted.hit(ten)
    busted.hit(five)

    hit = Hand(2)
    hit.hit(ten)
    hit.hit(five)

    player = HumanPlayer('Lloyd', 100)
    print(player)
    print(player.bet_or_leave())
    player.add_hand(blackjack)
    print(player.insurance(blackjack, ace))

    try:
        print(player.play(player.hands[0], ace))
    except AssertionError:
        print(f"Can't play {player.hands[0]}. Skipping")

    player = HumanPlayer('Lloyd', 100)
    player.add_hand(split)
    try:
        print(player.play(player.hands[0], ace))
    except AssertionError:
        print(f"Can't play {player.hands[0]}. Skipping")

    player = HumanPlayer('Lloyd', 100)
    player.add_hand(double)
    try:
        print(player.play(player.hands[0], ace))
    except AssertionError:
        print(f"Can't play {player.hands[0]}. Skipping")

    player = HumanPlayer('Lloyd', 100)
    player.add_hand(twentyone)
    try:
        print(player.play(player.hands[0], ace))
    except AssertionError:
        print(f"Can't play {player.hands[0]}. Skipping")

    player = HumanPlayer('Lloyd', 100)
    player.add_hand(busted)
    try:
        print(player.play(player.hands[0], ace))
    except AssertionError:
        print(f"Can't play {player.hands[0]}. Skipping")

