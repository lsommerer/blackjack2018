from virtualtable import VirtualTable
from sommererbots import SommererBotOne, SommererBotTwo
from shoe import Shoe
from copy import deepcopy

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

        for table in self.tables:
            for player in table.players:
                print(player)


def main():
    simulation = Simulation()

    table1 = VirtualTable(simulation)
    player1 = SommererBotOne()
    player1.sit(table1)

    table2 = VirtualTable(simulation)
    player2 = SommererBotTwo()
    player2.sit(table2)

    simulation.run()



main()