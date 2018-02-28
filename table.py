class Table(object):

    def __init__(self, **kwargs):
        self._players = []
        self._dealer = None

    def add_player(self, player):
        self._players.append(player)

    def add_dealer(self, dealer):
        self._dealer = dealer

    def leave_table(self, player):
        self._players.remove(player)

    def has_players(self):
        return len(self._players) > 0

    def shuffling_shoe(self):
        """
        This method is called by a dealer when they are shuffling. If you are
        simulating multiple dealers with the same shoe, you should replace all
        dealer's shoes at this time. If you are playing a single game, then
        no action is required.
        """
        pass

    def get_players(self):
        return self._players

    def get_dealer(self):
        return self._dealer

    players = property(get_players)
    dealer = property(get_dealer)