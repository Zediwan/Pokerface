import random
from .card import Card, Suit, Value
from . import gui

class Deck():
    def __init__(self) -> None:
        self._cards: list[Card] = [Card(value.name, suit.name) for value in Value for suit in Suit]
        self.cards: list[Card] = self._cards.copy()
        
    def shuffle(self) -> None:
        random.shuffle(self.cards)
        
    def draw(self, num: int  = 0) -> Card:
        return self.cards.pop(num)

    def reset(self) -> None:
        self.cards = self._cards.copy()
        self.shuffle()
    
    def __str__(self) -> str:
        title = "DECK OVERVIEW"
        string: str = "----- DECK OVERVIEW -----"
        for card in self.cards:
            string += card.__str__() + "\n"
        string += gui.DIVIDER
            