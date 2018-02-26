from table import Table

class Player(object):

    def __init__(self, name, money=100):
        self.name = name
        self._chips = money
        self._table = None
        self._hands = []
        self.isVerbose = False

    def __str__(self):
        s = f'{self.name} ${self._chips:0.2f}: '
        if self._hands:
            for hand in self._hands:
                s += f'\n {hand}'
        else:
            s+= 'No hands'
        return s

    def sit(self, table):
        """Add the player to the list of players at a table."""
        if type(table) == Table:
            self._table = table
            table.add_player(self)
        else:
            raise TypeError('Table parameter must be of type Table.')

    def add_hand(self, hand):
        self._hands.append(hand)

    def rake_in(self, amount):
        """Add any winnings to the player's money."""
        self._chips += amount

    def rake_out(self, amount):
        """Give money to the dealer."""
        if amount > self._chips:
            raise ValueError(f"Player needs more money. (has: ${self._chips:0.2f} needs: ${amount:0.2f})")
        self._chips -= amount
        return amount

    def discard_hands(self):
        self._hands = []

    def bet_or_leave(self):
        """
        At the start of each round the player can either bet by entering an amount
        to bet, sit this hand out by entering 0 for a bet, or leave the table by
        entering -1.
        """
        raise NotImplementedError("Please implment this in your subclass.")

    def wants_insurance(self):
        """
        Returns True if the player should buy insurance else return False.

        This procedure is called by the dealer after all players have bet and
        receives their cards and after the dealer has received his cards. It is
        only called if the dealer is showing an ace (the dealer might have blackjack).
        """
        raise NotImplementedError("Please implment this in your subclass.")

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
        raise NotImplementedError("Please implment this in your subclass.")


    def count(self, card):
        """
        THIS IS AN ABSTRACT METHOD! implement it in your subclass.

        This method will be called every time the dealer deals a card to anyone.
        """
        #
        # Use this if you want your player to count cards. The dealer will call this method
        # on the player and send it each card as the player would see them. You can create one
        # of more instance variables here for your other methods to access as needed.
        #
        pass


    def reset_count(self):
        """
        THIS IS AN ABSTRACT METHOD! implement it in your subclass.

        This method will be called for you every time the dealer shuffles the deck."""
        #
        # Use this if you are counting cards.
        #
        pass

    def get_money(self):
        return self._chips

    def get_hands(self):
        return self._hands

    money = property(get_money)
    hands = property(get_hands)
