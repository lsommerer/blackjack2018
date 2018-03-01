from asciimatics.effects import Print
from asciimatics.renderers import BarChart
from asciimatics.scene import Scene
from asciimatics.screen import Screen

from simulation import Simulation
from virtualtable import VirtualTable
from sommererbots import SommererBotOne, SommererBotTwo, SommererBotThree
from random import seed

def main():
    global simulation
    simulation = Simulation()
    seed(2)

    table1 = VirtualTable(simulation, False)
    player1 = SommererBotOne(100)
    player1.sit(table1)

    table2 = VirtualTable(simulation, False)
    player2 = SommererBotTwo(100)
    player2.sit(table2)

    table3 = VirtualTable(simulation, False)
    player3 = SommererBotThree(100)
    player3.sit(table3)

    simulation.switch_all_shoes()
    Screen.wrapper(graphs)
    simulation.results()

def graphs(screen):
    global simulation
    names = [simulation.tables[0].players[0].name,
             simulation.tables[1].players[0].name,
             simulation.tables[2].players[0].name]
    money = Print(screen,
              BarChart(14, 100, [money0, money1, money2],
                       char="=",
                       gradient=[(25, Screen.COLOUR_RED),
                                 (80, Screen.COLOUR_YELLOW),
                                 (100, Screen.COLOUR_GREEN)],
                       scale = 150,
                       labels=True,
                       axes=BarChart.X_AXIS,
                       intervals = 25,
                       keys = names),
              x=3, y=2, transparent=False, speed=2)

    won = Print(screen,
              BarChart(14, 25, [won0, won1, won2],
                       char="W",
                       keys = names,
                       scale = 200),
              x=3, y=20, transparent=False, speed=2)

    lost = Print(screen,
              BarChart(14, 15, [lost0, lost1, lost2],
                       char="L",
                       scale = 200),
              x=33, y=20, transparent=False, speed=2)

    pushed = Print(screen,
              BarChart(14, 15, [pushed0, pushed1, pushed2],
                       char="P",
                       scale = 100),
              x=53, y=20, transparent=False, speed=2)

    scenes = []
    scenes.append(Scene([money, won, lost, pushed], duration=200))
    while simulation.has_players():
        screen.play(scenes, repeat=False)


def money0():
    global simulation
    table = 0
    simulation.tables[table].dealer.take_bets()
    simulation.tables[table].dealer.deal()
    simulation.tables[table].dealer.offer_insurance()
    simulation.tables[table].dealer.play_hands()
    simulation.tables[table].dealer.play_own_hand()
    simulation.tables[table].dealer.payout_hands()
    return simulation.tables[table].players[0].money

def money1():
    global simulation
    table = 1
    simulation.tables[table].dealer.take_bets()
    simulation.tables[table].dealer.deal()
    simulation.tables[table].dealer.offer_insurance()
    simulation.tables[table].dealer.play_hands()
    simulation.tables[table].dealer.play_own_hand()
    simulation.tables[table].dealer.payout_hands()
    return simulation.tables[table].players[0].money

def money2():
    global simulation
    table = 2
    simulation.tables[table].dealer.take_bets()
    simulation.tables[table].dealer.deal()
    simulation.tables[table].dealer.offer_insurance()
    simulation.tables[table].dealer.play_hands()
    simulation.tables[table].dealer.play_own_hand()
    simulation.tables[table].dealer.payout_hands()
    return simulation.tables[table].players[0].money


def won0():
    global simulation
    table = 0
    return simulation.tables[table].players[0].timesWon

def won1():
    global simulation
    table = 1
    return simulation.tables[table].players[0].timesWon

def won2():
    global simulation
    table = 2
    return simulation.tables[table].players[0].timesWon

def lost0():
    global simulation
    table = 0
    return simulation.tables[table].players[0].timesLost

def lost1():
    global simulation
    table = 1
    return simulation.tables[table].players[0].timesLost

def lost2():
    global simulation
    table = 2
    return simulation.tables[table].players[0].timesLost

def pushed0():
    global simulation
    table = 0
    return simulation.tables[table].players[0].timesPushed

def pushed1():
    global simulation
    table = 1
    return simulation.tables[table].players[0].timesPushed

def pushed2():
    global simulation
    table = 2
    return simulation.tables[table].players[0].timesPushed


main()

