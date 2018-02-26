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
        if len(self._players) > 0:
            return True
        else:
            return False

    def get_players(self):
        return self._players

    def get_dealer(self):
        return self._dealer

    players = property(get_players)
    dealer = property(get_dealer)