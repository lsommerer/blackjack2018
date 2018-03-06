from asciimatics.effects import Print
from asciimatics.renderers import BarChart
from asciimatics.scene import Scene
from asciimatics.screen import Screen

from simulation import Simulation
from virtualtable import VirtualTable
from random import seed


#
# IMPORT YOUR BOT(S)
#
from sommererbots import SommererBotOne, SommererBotTwo, SommererBotThree
from kolliparabots import Ian
from ziembots import BadRachelBot

MAX_WON = 100
MAX_LOST = 200
MAX_PUSH = 50
MAX_MONEY = 300
STARTING_MONEY = 150

def main():
    global simulation
    simulation = Simulation()
    seed(5)

    #
    # ADD YOUR BOT(S) TO THE LIST
    #
    setup_bots(['BadRachelBot', 'BadRachelBot', 'SommererBotThree'])

    simulation.switch_all_shoes()
    Screen.wrapper(graphs)
    print('*\n* Final Statistics\n*\n')
    for table in simulation.tables:
        table.results()

def setup_bots(bots):
    """Execute these commands to setup each bot at a table."""
    global simulation
    for number, bot in enumerate(bots):
        number += 1
        exec(f'''
table{number} = VirtualTable(simulation)
player{number} = {bot}(STARTING_MONEY)
player{number}.sit(table{number})
              ''')


def graphs(screen):
    global simulation
    names = [table.players[0].name for table in simulation.tables]
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
              x=3, y=2, transparent=False, speed=1)

    won = Print(screen,
              BarChart(14, 25, [won0, won1, won2],
                       char="W",
                       keys = names,
                       labels=True,
                       axes=BarChart.X_AXIS,
                       intervals = MAX_WON,
                       scale = MAX_WON),
              x=3, y=20, transparent=False, speed=1)

    lost = Print(screen,
              BarChart(14, 15, [lost0, lost1, lost2],
                       char="L",
                       labels=True,
                       axes=BarChart.X_AXIS,
                       intervals = MAX_LOST,
                       scale = MAX_LOST),
              x=33, y=20, transparent=False, speed=1)

    pushed = Print(screen,
              BarChart(14, 15, [pushed0, pushed1, pushed2],
                       char="P",
                       labels=True,
                       axes=BarChart.X_AXIS,
                       intervals = MAX_PUSH,
                       scale = MAX_PUSH),
              x=53, y=20, transparent=False, speed=1)

    scenes = []
    scenes.append(Scene([money, won, lost, pushed], duration=50))
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
        if simulation.tables[table].has_players():
            money = simulation.tables[table].players[0].money
        else:
            money = simulation.tables[table].finishedPlayers[0].money
        if money > MAX_MONEY:
            money = MAX_MONEY
    except:
        money = 0
        if simulation.tables[table].has_players():
            simulation.tables[table].players[0].timesAbend += 1
        else:
            simulation.tables[table].finishedPlayers[0].timesAbend += 1
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
        if simulation.tables[table].has_players():
            money = simulation.tables[table].players[0].money
        else:
            money = simulation.tables[table].finishedPlayers[0].money
        if money > MAX_MONEY:
            money = MAX_MONEY
    except:
        money = 0
        if simulation.tables[table].has_players():
            simulation.tables[table].players[0].timesAbend += 1
        else:
            simulation.tables[table].finishedPlayers[0].timesAbend += 1
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
        if simulation.tables[table].has_players():
            money = simulation.tables[table].players[0].money
        else:
            money = simulation.tables[table].finishedPlayers[0].money
        if money > MAX_MONEY:
            money = MAX_MONEY
    except:
        money = 0
        if simulation.tables[table].has_players():
            simulation.tables[table].players[0].timesAbend += 1
        else:
            simulation.tables[table].finishedPlayers[0].timesAbend += 1
    return money


def won0():
    global simulation
    table = 0
    if simulation.tables[table].has_players():
        won = simulation.tables[table].players[0].timesWon
    else:
        won = simulation.tables[table].finishedPlayers[0].timesWon
    if won > MAX_WON:
        won = MAX_WON
    return won

def won1():
    global simulation
    table = 1
    if simulation.tables[table].has_players():
        won = simulation.tables[table].players[0].timesWon
    else:
        won = simulation.tables[table].finishedPlayers[0].timesWon
    if won > MAX_WON:
        won = MAX_WON
    return won

def won2():
    global simulation
    table = 2
    if simulation.tables[table].has_players():
        won = simulation.tables[table].players[0].timesWon
    else:
        won = simulation.tables[table].finishedPlayers[0].timesWon
    if won > MAX_WON:
        won = MAX_WON
    return won

def lost0():
    global simulation
    table = 0
    if simulation.tables[table].has_players():
        lost = simulation.tables[table].players[0].timesLost
    else:
        lost = simulation.tables[table].finishedPlayers[0].timesLost
    if lost > MAX_LOST:
        lost = MAX_LOST
    return lost

def lost1():
    global simulation
    table = 1
    if simulation.tables[table].has_players():
        lost = simulation.tables[table].players[0].timesLost
    else:
        lost = simulation.tables[table].finishedPlayers[0].timesLost
    if lost > MAX_LOST:
        lost = MAX_LOST
    return lost

def lost2():
    global simulation
    table = 2
    if simulation.tables[table].has_players():
        lost = simulation.tables[table].players[0].timesLost
    else:
        lost = simulation.tables[table].finishedPlayers[0].timesLost
    if lost > MAX_LOST:
        lost = MAX_LOST
    return lost

def pushed0():
    global simulation
    table = 0
    if simulation.tables[table].has_players():
        pushed = simulation.tables[table].players[0].timesPushed
    else:
        pushed = simulation.tables[table].finishedPlayers[0].timesPushed
    if pushed > MAX_PUSH:
        pushed = MAX_PUSH
    return pushed

def pushed1():
    global simulation
    table = 1
    if simulation.tables[table].has_players():
        pushed = simulation.tables[table].players[0].timesPushed
    else:
        pushed = simulation.tables[table].finishedPlayers[0].timesPushed
    if pushed > MAX_PUSH:
        pushed = MAX_PUSH
    return pushed

def pushed2():
    global simulation
    table = 2
    if simulation.tables[table].has_players():
        pushed = simulation.tables[table].players[0].timesPushed
    else:
        pushed = simulation.tables[table].finishedPlayers[0].timesPushed
    if pushed > MAX_PUSH:
        pushed = MAX_PUSH
    return pushed


main()

