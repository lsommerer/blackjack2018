class Table(object):

    def __init__(self):
        self._players = []
        self._dealer = None

    def add_player(self, player):
        self._players.append(player)

    def add_dealer(self, dealer):
        self._dealer = dealer

    def leave_table(self, player):
        del self._players[player]