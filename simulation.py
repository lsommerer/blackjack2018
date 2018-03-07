from virtualtable import VirtualTable
from shoe import Shoe
from copy import deepcopy
from random import seed

from bots import SommererBotThree, IanThree, GlinesBotThree, RichBot, BadRachelBot2, TessaBot, StreichBotOne


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
                if player.money > 1:
                    hasPlayers = True
        return hasPlayers

    def run(self):
        x = 1
        while self.has_players():# and x < 10000:
            for table in self.tables:
                table.dealer.take_bets()
                table.dealer.deal()
                table.dealer.offer_insurance()
                table.dealer.play_hands()
                table.dealer.play_own_hand()
                table.dealer.payout_hands()
                x += 1
                if x % 2000 == 0: self.quick_results()

    def quick_results(self):
        print()
        for table in self.tables:
            for player in table.players:
                print(f'${player.totalWagers:0.2f} ${player.money:0.2f} ({player.name}) ')

    def reset_bots(self, newMoney):
        print(f'*************** RESETTING BOTS WITH ${money:0.2f} *************')
        for table in self.tables:
            for player in table.players:
                player.rake_out(player.money)
                player.rake_in(newMoney)
        self.quick_results()


    def results(self):
        print('*\n* Final Statistics\n*\n')
        for table in self.tables:
            for player in table.players:
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



def main():
    seedNumber = 500
    seed(seedNumber)
    amounts = [25, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500]
    global simulation
    simulation = Simulation()

    setup_bots(10, ['StreichBotOne', 'RichBot', 'BadRachelBot2', 'TessaBot', 'GlinesBotThree', 'IanThree'])

    for money in amounts:
        simulation.switch_all_shoes()
        simulation.run()
        simulation.reset_bots(money)
        seed(seedNumber + money)
    #simulation.results()


def setup_bots(money, bots):
    """Execute these commands to setup each bot at a table."""
    global simulation
    for number, bot in enumerate(bots):
        number += 1
        exec(f'''
table{number} = VirtualTable(simulation)
player{number} = {bot}({money})
player{number}.sit(table{number})''')


if __name__ == '__main__':
    main()
