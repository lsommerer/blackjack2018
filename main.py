def main():
    table = Table(doubleOn=[9,10,11])
    dealer = Dealer()
    dealer.sit(table)
    for number in range(1,numberOfPlayers):
        player = Player(f'player{number}',100)
        player.sit(table)
    dealer.take_bets()
    while table.has_players():
        dealer.deal()
        dealer.offer_insurance()
        dealer.offer_surrender()
        dealer.resolve_hands()
        dealer.payout()
        dealer.take_bets()

