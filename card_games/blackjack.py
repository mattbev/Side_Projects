import deck.deck as deck

class BlackJack:

    values = {
        "A*" : 1,
        "2" : 2,
        "3" : 3,
        "4" : 4,
        "5" : 5,
        "6" : 6,
        "7" : 7,
        "8" : 8,
        "9" : 9,
        "10" : 10,
        "J" : 10,
        "Q" : 10,
        "K" : 10,
        "A" : 11
    }

    def __init__(self, num_players=1, betting=False, buy_in=100, num_decks=6):
        self.betting = betting
        self.buy_in = buy_in
        self.num_decks = num_decks
        self.players = [Player(i, self.buy_in) for i in range(num_players)]
        self.dealer = Dealer(-1)

    def deal_hand(self, num_decks):
        self.in_play = [player for player in self.players]
        self.deck = deck.Deck(num_decks)
        for player in self.players:
            player.new_hand()
            player.add_card(self.deck.draw_card())
            player.add_card(self.deck.draw_card())
        self.dealer.new_hand()
        self.dealer.add_card(self.deck.draw_card())
        self.dealer.add_card(self.deck.draw_card())

    def check_status(self, player):
        if player.get_count() > 21:
            cards = player.cards
            for card in cards:
                if card.value == "A":
                    card.set_value("A*")
                    player.display()
                    return
            BlackJack.print_bust()
            player.bust = True
            if type(player) == Player and player in self.in_play:
                self.in_play.remove(player)

    def hit(self, player):
        player.add_card(self.deck.draw_card())
        player.display()

    def stand(self, player):
        self.in_play.remove(player)

    def take_bets(self):
        for player in self.players:
            BlackJack.print_bank(player)
            bet = input("place bet: ")
            while type(bet) is not int:
                try:
                    bet = int(bet)
                    assert 0 <= bet <= player.bank.available
                except:
                    bet = input("place bet: ")
            player.bank.place_bet(bet)
            BlackJack.print_line()

    def double_down(self, player):
        player.bank.place_bet(min(player.bank.available, player.bank.bet))
        self.hit(player)
        if player.bust is False:
            self.stand(player)

    def end_hand(self):
        self.dealer.display()
        while self.dealer.get_count() <= 16:
            self.hit(self.dealer)
            self.check_status(self.dealer)

        score_to_beat = self.dealer.get_count() if self.dealer.bust is False else 0
        blackjack_winners = []
        ties = []
        winners = []
        losers = []
        for player in self.players:
            if player.bust is False and player.get_count() > score_to_beat:
                if player.get_count() == 21:
                    blackjack_winners.append(player)
                else:
                    winners.append(player)
            elif player.bust is False and player.get_count() == score_to_beat:
                ties.append(player)
            else:
                losers.append(player)

        BlackJack.print_line()
        BlackJack.print_results(blackjack_winners, ties, winners, losers)
        BlackJack.payouts(blackjack_winners, ties, winners, losers)

    def play(self):
        table_open = True
        while table_open:
            valid_inputs = {"hit", "stand", "double"}
            self.take_bets()
            self.deal_hand(self.num_decks)
            self.dealer.display_beginning()
            BlackJack.print_line()
            while self.in_play:
                for player in self.in_play:
                    player.display()
                    action = input("action (hit, stand, double): ").lower()
                    while action not in valid_inputs:
                        action = input("action (hit, stand, double): ").lower()
                    if action == "hit":
                        self.hit(player)
                    elif action == "stand":
                        self.stand(player)
                    # elif action == "split":
                    #     self.split(player)
                    elif action == "double":
                        self.double_down(player)
                    self.check_status(player)
                    BlackJack.print_line()

            self.end_hand()
            next_hand = input("next hand? (y/n): ")
            if next_hand == "n":
                table_open = False
                self.in_play = True
            BlackJack.print_line()

    @staticmethod
    def print_line():
        print("-------------------------------------------------------")

    @staticmethod
    def print_results(blackjack_winners, ties, winners, losers):
        print("blackjack win:", [player.name for player in blackjack_winners])
        print("tie:", [player.name for player in ties])
        print("win:", [player.name for player in winners])
        print("lose:", [player.name for player in losers])

    @staticmethod
    def print_bust():
        print("bust!")

    @staticmethod
    def payouts(blackjack_winners, ties, winners, losers):
        for player in blackjack_winners:
            player.bank.blackjack()
        for player in ties:
            player.bank.tie()
        for player in winners:
            player.bank.win()
        for player in losers:
            player.bank.loss()

    @staticmethod
    def print_bank(player):
        print("player " + str(player.name) + ", available: ", player.bank.available)


class Player:

    def __init__(self, name, money=0):
        self.name = name
        self.cards = []
        self.bust = False
        self.bank = Bank(self, money)


    def add_card(self, card):
        self.cards.append(card)

    def new_hand(self):
        self.cards = []
        self.bust = False

    def get_count(self):
        count = 0
        for card in self.cards:
            count += BlackJack.values[card.value]
        return count

    def display(self):
        print(self.__str__())

    def __str__(self):
        return "player " + str(self.name) + ": " + str(self.get_count()) + " " + str([card.__str__() for card in self.cards])


class Dealer(Player):

    def display_beginning(self):
        print("dealer: " + str(self.cards[0].__str__()))

    def display(self):
        print("dealer: " + str(self.get_count()) + " " + str([card.__str__() for card in self.cards]))


class Bank:
    def __init__(self, player, available):
        self.player = player
        self.available = available
        self.bet = 0

    def place_bet(self, amount):
        bet = max(0, min(amount, self.available))
        self.available -= bet
        self.bet += bet

    def win(self):
        self.available += 2*self.bet
        self.bet = 0

    def tie(self):
        self.available += self.bet
        self.bet = 0

    def loss(self):
        self.bet = 0

    def blackjack(self):
        self.available += 2.5*self.bet
        self.bet = 0


if __name__ == "__main__":
    BlackJack(1).play()

