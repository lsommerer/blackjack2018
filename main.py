from table import Table
from dealer import Dealer
from humanplayer import HumanPlayer
from toolbox import get_integer_between, get_string
from card import Card

def main():
    print('---Blackjack 0.5---\n')
    table = Table(doubleOn=[9,10,11])
    dealer = Dealer('Dealer', 1000000)
    dealer.sit(table)
    #
    # Deck Stacking:
    #
    dealer._shoe.append(Card('ace', 'spades'))
    dealer._shoe.append(Card('ace', 'hearts'))
    #
    #
    #
    numberOfPlayers = get_integer_between(1, 7, 'How many players?')
    for number in range(1,numberOfPlayers+1):
        name = get_string(f"What is player {number}'s name?")
        player = HumanPlayer(name,100)
        player.sit(table)
    dealer.take_bets()
    while table.has_players():
        dealer.deal()
        dealer.offer_insurance()
        dealer.play_hands()
        dealer.play_own_hand()
        dealer.payout_hands()
        dealer.take_bets()
    print('\n---There are no more players. Game Over.---')

main()
