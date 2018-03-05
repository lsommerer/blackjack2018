from asciimatics.effects import Print
from asciimatics.renderers import BarChart
from asciimatics.scene import Scene
from asciimatics.screen import Screen

from simulation import Simulation
from virtualtable import VirtualTable
from sommererbots import SommererBotOne, SommererBotTwo, SommererBotThree
from kolliparabots import Ian
from random import seed

MAX_WON = 100
MAX_LOST = 200
MAX_PUSH = 50
MAX_MONEY = 300
STARTING_MONEY = 150

def main():
    global simulation
    simulation = Simulation()
    seed(2)

    table1 = VirtualTable(simulation)
    player1 = Ian(STARTING_MONEY)
    player1.sit(table1)

    table2 = VirtualTable(simulation)
    player2 = SommererBotTwo(STARTING_MONEY)
    player2.sit(table2)

    table3 = VirtualTable(simulation)
    player3 = SommererBotThree(STARTING_MONEY)
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
                       gradient=[(STARTING_MONEY/4, Screen.COLOUR_RED),
                                 (STARTING_MONEY/4*3, Screen.COLOUR_YELLOW),
                                 (STARTING_MONEY, Screen.COLOUR_WHITE),
                                 (MAX_MONEY, Screen.COLOUR_GREEN)],
                       scale = MAX_MONEY,
                       labels=True,
                       axes=BarChart.X_AXIS,
                       intervals = MAX_MONEY/4,
                       keys = names),
              x=3, y=2, transparent=False, speed=2)

    won = Print(screen,
              BarChart(14, 25, [won0, won1, won2],
                       char="W",
                       keys = names,
                       labels=True,
                       axes=BarChart.X_AXIS,
                       intervals = MAX_WON,
                       scale = MAX_WON),
              x=3, y=20, transparent=False, speed=2)

    lost = Print(screen,
              BarChart(14, 15, [lost0, lost1, lost2],
                       char="L",
                       labels=True,
                       axes=BarChart.X_AXIS,
                       intervals = MAX_LOST,
                       scale = MAX_LOST),
              x=33, y=20, transparent=False, speed=2)

    pushed = Print(screen,
              BarChart(14, 15, [pushed0, pushed1, pushed2],
                       char="P",
                       labels=True,
                       axes=BarChart.X_AXIS,
                       intervals = MAX_PUSH,
                       scale = MAX_PUSH),
              x=53, y=20, transparent=False, speed=2)

    scenes = []
    scenes.append(Scene([money, won, lost, pushed], duration=200))
    while simulation.has_players():
        screen.play(scenes, repeat=False)


def money0():
    global simulation
    table = 0
    try:
        simulation.tables[table].dealer.take_bets()
        simulation.tables[table].dealer.deal()
        simulation.tables[table].dealer.offer_insurance()
        simulation.tables[table].dealer.play_hands()
        simulation.tables[table].dealer.play_own_hand()
        simulation.tables[table].dealer.payout_hands()
        money = simulation.tables[table].players[0].money
        if money > MAX_MONEY:
            money = MAX_MONEY
    except:
        money = 0
        simulation.tables[table].players[0].timesAbend += 1
    return money

def money1():
    global simulation
    table = 1
    try:
        simulation.tables[table].dealer.take_bets()
        simulation.tables[table].dealer.deal()
        simulation.tables[table].dealer.offer_insurance()
        simulation.tables[table].dealer.play_hands()
        simulation.tables[table].dealer.play_own_hand()
        simulation.tables[table].dealer.payout_hands()
        money = simulation.tables[table].players[0].money
        if money > MAX_MONEY:
            money = MAX_MONEY
    except:
        money = 0
        simulation.tables[table].players[0].timesAbend += 1
    return money

def money2():
    global simulation
    table = 2
    try:
        simulation.tables[table].dealer.take_bets()
        simulation.tables[table].dealer.deal()
        simulation.tables[table].dealer.offer_insurance()
        simulation.tables[table].dealer.play_hands()
        simulation.tables[table].dealer.play_own_hand()
        simulation.tables[table].dealer.payout_hands()
        money = simulation.tables[table].players[0].money
        if money > MAX_MONEY:
            money = MAX_MONEY
    except:
        money = 0
        simulation.tables[table].players[0].timesAbend += 1
    return money


def won0():
    global simulation
    table = 0
    won = simulation.tables[table].players[0].timesWon
    if won > MAX_WON:
        won = MAX_WON
    return won

def won1():
    global simulation
    table = 1
    won = simulation.tables[table].players[0].timesWon
    if won > MAX_WON:
        won = MAX_WON
    return won

def won2():
    global simulation
    table = 2
    won = simulation.tables[table].players[0].timesWon
    if won > MAX_WON:
        won = MAX_WON
    return won

def lost0():
    global simulation
    table = 0
    lost = simulation.tables[table].players[0].timesWon
    if lost > MAX_LOST:
        lost = MAX_LOST
    return lost

def lost1():
    global simulation
    table = 1
    lost = simulation.tables[table].players[0].timesWon
    if lost > MAX_LOST:
        lost = MAX_LOST
    return lost

def lost2():
    global simulation
    table = 2
    lost = simulation.tables[table].players[0].timesLost
    if lost > MAX_LOST:
        lost = MAX_LOST
    return lost

def pushed0():
    global simulation
    table = 0
    pushed = simulation.tables[table].players[0].timesPushed
    if pushed > MAX_PUSH:
        pushed = MAX_PUSH
    return pushed

def pushed1():
    global simulation
    table = 1
    pushed = simulation.tables[table].players[0].timesPushed
    if pushed > MAX_PUSH:
        pushed = MAX_PUSH
    return pushed

def pushed2():
    global simulation
    table = 2
    pushed = simulation.tables[table].players[0].timesPushed
    if pushed > MAX_PUSH:
        pushed = MAX_PUSH
    return pushed


main()

