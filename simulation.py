from virtualtable import VirtualTable
from sommererbots import SommererBotOne, SommererBotTwo
from shoe import Shoe
from copy import deepcopy
from random import seed

class Simulation(object):

    def __init__(self):
        self.tables = []

    def add_table(self, table):
        self.tables.append(table)

    def switch_all_shoes(self):
        """
        When any table calls this method, give a new, identical shoe to each
        table in the simulation.
        :return:
        """
        shoe = Shoe()
        for table in self.tables:
            table._dealer.switch_shoe(deepcopy(shoe))

    def has_players(self):
        hasPlayers = False
        for table in self.tables:
            for player in table.players:
                if player.money > 0:
                    hasPlayers = True
        return hasPlayers

    def run(self):
        numberOfRounds = 1000
        while self.has_players():
            for table in self.tables:
                table.dealer.take_bets()
                table.dealer.deal()
                table.dealer.offer_insurance()
                table.dealer.play_hands()
                table.dealer.play_own_hand()
                table.dealer.payout_hands()

    def results(self):
        for table in self.tables:
            for player in table.players:
                print(player)
                print(f"   hands:      {player.handsPlayed}")
                print(f"   wagers:    ${player.totalWagers:0.2f} (${player.totalWagers/player.handsPlayed:0.2f}/hand)")
                print()
                print(f"   hit:        {player.timesHit} ({player.timesHit/player.handsPlayed} per hand)")
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

def main():
    seed(1)
    simulation = Simulation()

    table1 = VirtualTable(simulation)
    player1 = SommererBotOne()
    player1.sit(table1)

    table2 = VirtualTable(simulation)
    player2 = SommererBotTwo()
    player2.sit(table2)

    simulation.switch_all_shoes()
    simulation.run()
    simulation.results()



main()