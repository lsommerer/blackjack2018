from table import Table
from dealer import Dealer

class VirtualTable(Table):
    """
    This Table Class is for use when you are simulating blackjack games to test various player types.
    """

    def __init__(self, simulation):
        super().__init__()
        simulation.add_table(self)
        self._simulation = simulation
        self.finishedPlayers = []
        bankroll = 1_000_000
        delay = 0
        verbose = False
        dealer = Dealer('Dealer', bankroll, delay, verbose)
        dealer.sit(self)

    def has_active_players(self):
        hasActivePlayers = False
        for player in self.players:
            if player.money >= 1:
                hasActivePlayers = True
        return hasActivePlayers

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
        #self.finishedPlayers.append(player)
        #self.players.remove(player)
        pass

    def results(self):
        for player in self.finishedPlayers:
            print(player)
            print(f"   hands:      {player.handsPlayed}")
            print(f"   wagers:    ${player.totalWagers:0.2f} (${player.totalWagers/player.handsPlayed:0.2f}/hand)")
            print(f"   abends:    {player.timesAbend} ({player.timesAbend/player.handsPlayed:0.2f}/hand)")
            print()
            print(f"   hit:        {player.timesHit} ({player.timesHit/player.handsPlayed:0.2f} per hand)")
            print(f"   split:      {player.timesSplit} ({player.timesSplit/player.handsPlayed*100:.0f}% of the time)")
            print(f"   doubled:    {player.timesDoubled} ({player.timesDoubled/player.handsPlayed*100:.0f}% of the time)")
            print()
            print(f"   blackjack!: {player.timesBlackjack} ({player.timesBlackjack/player.handsPlayed*100:.0f}% of the time)")
            print(f"   busted:     {player.timesBusted} ({player.timesBusted/player.handsPlayed*100:.0f}% of the time)")
            print()
            print(f"   won:        {player.timesWon} ({player.timesWon/player.handsPlayed*100:.0f}% of the time)")
            print(f"   lost:       {player.timesLost} ({player.timesLost/player.handsPlayed*100:.0f}% of the time)")
            print(f"   pushed:     {player.timesPushed} ({player.timesPushed/player.handsPlayed*100:.0f}% of the time)")
            print()
            print(f"   insurance:  {player.timesInsurance} ({player.timesInsurance/player.handsPlayed*100:.0f}% of the time)")
            print(f"   surrender:  {player.timesSurrendered} ({player.timesSurrendered/player.handsPlayed*100:.0f}% of the time)")
            print()
