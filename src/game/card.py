from enum import Enum

class Value(Enum):
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    TEN = "10"
    JACK = "J"
    QUEEN = "Q"
    KING = "K"
    ACE = "A"

class Suit(Enum):
    HEARTS = "♥️"
    DIAMONDS = "♦️"
    CLUBS = "♣️"
    SPADES = "♠️"

class Card():
    def __init__(self, value: Value, suit: Suit) -> None:
        self.value: Value = value
        self.suit: Suit = suit
    
    def __str__(self) -> str:
        return "|" + Value[self.value].value.__str__() + Suit[self.suit].value + "|"