from table import Table
from dealer import Dealer
from humanplayer import HumanPlayer

def main():
    table = Table(doubleOn=[9,10,11])
    dealer = Dealer('Bob the Dealer', 1000000)
    dealer.sit(table)
    numberOfPlayers = 1
    for number in range(1,numberOfPlayers+1):
        player = HumanPlayer(f'player{number}',100)
        player.sit(table)
        print(player)
    dealer.take_bets()
    while table.has_players():
        dealer.deal()
        dealer.offer_insurance()
        dealer.play_hands()
        dealer.play_own_hand()
        dealer.payout_hands()
        dealer.take_bets()

main()
