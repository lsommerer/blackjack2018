from table import Table
from dealer import Dealer

class VirtualTable(Table):
    """
    This Table Class is for use when you are simulating blackjack games to test various player types.
    """

    def __init__(self, simulation, verbose = True):
        super().__init__()
        simulation.add_table(self)
        self._simulation = simulation
        dealer = Dealer('Dealer', 100000, 0)
        dealer.isVerbose = verbose
        dealer.sit(self)

    def shuffling_shoe(self):
        """
        Dealer is shuffling his shoe. Since we want all dealers in the simulation to use the same shoes,
        Ask the simulation for a new shoe and give it to the dealer.
        :return:
        """
        self._simulation.switch_all_shoes()


    def leave_table(self, player):
        """
        This might cause problems for the simulation, so just leave them at the table.

        :param player:
        :return:
        """
        pass