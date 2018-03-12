from virtualtable import VirtualTable
from shoe import Shoe
from copy import copy, deepcopy
from random import seed
import cProfile

#
# IMPORT your bots from wherever you keep them, then update the list of bots below.
#
from allbots import SommererBotBasicStrategy, \
                    IanFour, \
                    StreichBotSeven, \
                    NhuBlackjackBotOne, \
                    GlinesBotFour, \
                    RichBotTwo, \
                    BadRachelBot5, \
                    TessaBot

def main():
    seedNumber = 355
    seed(seedNumber)
    amounts = [25, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500]
    bots = [SommererBotBasicStrategy, StreichBotSeven, RichBotTwo, BadRachelBot5, TessaBot, GlinesBotFour, NhuBlackjackBotOne]

    global simulation
    simulation = Simulation(bots)

    for money in amounts:
        simulation.reset_bots(money)
        seed(seedNumber + money)
        simulation.run()
    simulation.results()
    simulation.results_chart()


class Simulation(object):

    def __init__(self, botList):
        self.tables = []
        self.handsPlayed = 0
        self.currentStartingMoney = 0
        for bot in botList:
            table = VirtualTable(self)
            money = 0
            player = bot(money)
            player.sit(table)

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
            if table.has_active_players():
                table._dealer.switch_shoe(deepcopy(shoe))


    def has_players(self):
        """Are there any players at any tables with money left to bet?"""
        hasPlayers = False
        for table in self.tables:
            for player in table.players:
                if player.money > 1:
                    hasPlayers = True
        return hasPlayers

    def run(self):
        while self.has_players():
            for table in self.tables:
                table.dealer.take_bets()
                table.dealer.deal()
                table.dealer.offer_insurance()
                table.dealer.play_hands()
                table.dealer.play_own_hand()
                table.dealer.payout_hands()
            self.handsPlayed += 1
            if self.handsPlayed % 1000 == 0: self.quick_results()


    def quick_results(self):
        print(f'\n*** Results after {self.handsPlayed} potential hands (${self.currentStartingMoney:0.2f} in chips) ***')
        print('Total Wagered  Current      Max   Name')
        for table in self.tables:
            for player in table.players:
                print(f'{player.totalWagers:13,.2f} {player.money:8,.2f} {player.maxMoney:8,.2f}   {player.name:18}')

    def reset_bots(self, newMoney):
        print(f'*************** RESETTING BOTS WITH ${newMoney:0.2f} *************')
        self.currentStartingMoney = newMoney
        for table in self.tables:
            for player in table.players:
                player.rake_out(player.money)
                player.rake_in(newMoney)
                player.maxMoney = 0
                player.lastHand = None
        self.switch_all_shoes()

    def results(self):
        print('\n*** Final Statistics ***\n\n')
        totalhands = 0
        for table in self.tables:
            for player in table.players:
                print(player)
                print(f"   hands:      {player.handsPlayed}")
                print(f"   wagers:    ${player.totalWagers:0.2f} (${player.totalWagers/player.handsPlayed:0.2f}/hand)")
                print(f"   abends:    {player.timesAbend} ({player.timesAbend/player.handsPlayed:0.2f}/hand)")
                print()
                print(f"   hit:        {player.timesHit} ({player.timesHit/player.handsPlayed:0.2f} per hand)")
                print(
                    f"   split:      {player.timesSplit} ({player.timesSplit/player.handsPlayed*100:.0f}% of the time)")
                print(
                    f"   doubled:    {player.timesDoubled} ({player.timesDoubled/player.handsPlayed*100:.0f}% of the time)")
                print()
                print(
                    f"   blackjack!: {player.timesBlackjack} ({player.timesBlackjack/player.handsPlayed*100:.0f}% of the time)")
                print(
                    f"   busted:     {player.timesBusted} ({player.timesBusted/player.handsPlayed*100:.0f}% of the time)")
                print()
                print(f"   won:        {player.timesWon} ({player.timesWon/player.handsPlayed*100:.0f}% of the time)")
                print(f"   lost:       {player.timesLost} ({player.timesLost/player.handsPlayed*100:.0f}% of the time)")
                print(
                    f"   pushed:     {player.timesPushed} ({player.timesPushed/player.handsPlayed*100:.0f}% of the time)")
                print()
                print(
                    f"   insurance:  {player.timesInsurance} ({player.timesInsurance/player.handsPlayed*100:.0f}% of the time)")
                print(
                    f"   surrender:  {player.timesSurrendered} ({player.timesSurrendered/player.handsPlayed*100:.0f}% of the time)")
                print()
                totalhands += player.handsPlayed
        print(f'Actual hands played: {totalhands}')


    def results_chart(self):
        print('\n*** Final Statistics ***\n\n')
        totalhands = 0
        print('Name                      Wagers     (Avg)    Hands   Avg Hits  Split%   Doubled%  Blackjack%   Bust%  Won%   Lost%   Push%  Insure% Abends')
        print('-------------------------------------------------------------------------------------------------------------------------------------------')
        for table in self.tables:
            for player in table.players:
                string = ''
                string += f'{player.name:18}:'
                string += f'{player.totalWagers:13,.2f}   '
                string += f'${player.totalWagers/player.handsPlayed:6.2f}'
                string += f'{player.handsPlayed:9}      '
                string += f'{player.timesHit/player.handsPlayed:5.2f}     '
                string += f'{player.timesSplit/player.handsPlayed*100:2.0f}%        '
                string += f'{player.timesDoubled/player.handsPlayed*100:2.0f}%         '
                string += f'{player.timesBlackjack/player.handsPlayed*100:2.0f}%     '
                string += f'{player.timesBusted/player.handsPlayed*100:2.0f}%   '
                string += f'{player.timesWon/player.handsPlayed*100:2.0f}%     '
                string += f'{player.timesLost/player.handsPlayed*100:2.0f}%     '
                string += f'{player.timesPushed/player.handsPlayed*100:2.0f}%      '
                string += f'{player.timesInsurance/player.handsPlayed*100:2.0f}%    '
                string += f'{player.timesAbend:3}  '
                #string += f'{player.timesSurrendered/player.handsPlayed*100:.0f}%  '
                print(string)
                totalhands += player.handsPlayed
        print('-------------------------------------------------------------------------------------------------------------------------------------------')
        print(f'Actual hands played: {totalhands}')



if __name__ == '__main__':
    #cProfile.run('main()')
    main()
