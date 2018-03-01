from asciimatics.effects import Print
from asciimatics.renderers import BarChart
from asciimatics.scene import Scene
from asciimatics.screen import Screen

from simulation import Simulation
from virtualtable import VirtualTable
from sommererbots import SommererBotOne, SommererBotTwo, SommererBotThree
from random import seed


def fn0():
    global simulation
    table = 0
    simulation.tables[table].dealer.take_bets()
    simulation.tables[table].dealer.deal()
    simulation.tables[table].dealer.offer_insurance()
    simulation.tables[table].dealer.play_hands()
    simulation.tables[table].dealer.play_own_hand()
    simulation.tables[table].dealer.payout_hands()
    return simulation.tables[table].players[0].money

def fn1():
    global simulation
    table = 1
    simulation.tables[table].dealer.take_bets()
    simulation.tables[table].dealer.deal()
    simulation.tables[table].dealer.offer_insurance()
    simulation.tables[table].dealer.play_hands()
    simulation.tables[table].dealer.play_own_hand()
    simulation.tables[table].dealer.payout_hands()
    return simulation.tables[table].players[0].money

def fn2():
    global simulation
    table = 2
    simulation.tables[table].dealer.take_bets()
    simulation.tables[table].dealer.deal()
    simulation.tables[table].dealer.offer_insurance()
    simulation.tables[table].dealer.play_hands()
    simulation.tables[table].dealer.play_own_hand()
    simulation.tables[table].dealer.payout_hands()
    return simulation.tables[table].players[0].money

def graphs(screen):
    global simulation
    if screen.width != 132 or screen.height != 24:
        raise ValueError("Resize terminal to 132x24")
    else:
        names = [simulation.tables[0].players[0].name,
                 simulation.tables[1].players[0].name,
                 simulation.tables[2].players[0].name]
        graph = Print(screen,
                  BarChart(15, 100, [fn0, fn1, fn2],
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

        scenes = []
        scenes.append(Scene([graph], duration=200))
        while simulation.has_players():
            screen.play(scenes, repeat=False)

def main():
    global simulation
    simulation = Simulation()
    seed(1)

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

main()

