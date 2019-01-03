import random

class Deck:
    def __init__(self, num_decks=1):
        self.deck = Deck.create_deck(num_decks)

    @staticmethod
    def create_deck(num_decks):
        suit_names = ['Spades', 'Diamonds', 'Hearts', 'Clubs']
        deck = set()
        for deck_number in range(num_decks):
            for suit in suit_names:
                deck = deck.union({Card(suit, str(x)) for x in range(2, 11)}.union({Card(suit, y) for y in {"J", "Q", "K", "A"}}))
        return deck

    def num_cards(self):
        return len(self.deck)

    def draw_card(self):
        card = random.choice(tuple(self.deck))
        self.deck.remove(card)
        return card

    def add_card(self, card):
        self.deck.add(card)

    def __str__(self):
        return list(card.__str__() for card in self.deck)


class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def set_value(self, val):
        self.value = val

    def __str__(self):
        return str((self.suit, self.value))