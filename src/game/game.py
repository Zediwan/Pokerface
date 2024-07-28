from .player import Player, InsufficientMoneyError, OutOfMoneyError
from .deck import Deck
from .card import Card
from . import game_rules

class Game():
    def __init__(self) -> None:
        self._small_blind_index = 0
        self.players: list[Player] = []
        self.deck = Deck()
    
    @property
    def small_blind_index(self) -> int:
        return self._small_blind_index

    @small_blind_index.setter
    def small_blind_index(self, new_index: int) -> None:
        if new_index >= len(self.players):
            self._small_blind_index = 0
        else:
            self._small_blind_index = new_index
    
    @property
    def big_blind_index(self) -> int:
        if self.small_blind_index == len(self.players) - 1:
            return 0
        else:
            return self.small_blind_index + 1
    
    def add_player(self, player: Player) -> None:
        self.players.append(player)
        player.money = game_rules.STARTING_MONEY
    
    def remove_player(self, player: Player) -> None:
        self.players.remove(player)
        print(f"[i] {player.name} has been removed from the game")

    def play_round(self) -> None:
        bet = 0
        players = self.players.copy()
        table_cards: list[Card] = []
        
        # Set blinds
        self._set_blinds()
    
    def _set_blinds(self) -> None:
        self._set_small_blind()
        self._set_big_blind()
    
    def _set_small_blind(self) -> None:
        """
        Sets the small blind for the current round of the game.

        This method selects the player who will be the small blind for the current round
        and deducts the small blind amount from their money. If the player does not have
        enough money to pay the small blind, they are removed from the game.

        If there is only one player remaining, the game is considered over. \n
        If the small blind cannot be set, the method is called recursively
        until a valid small blind is set or the game is over.
        """
        small_blind = self.players[self.small_blind_index]
        done = False
        
        # Try to remove the money
        try:
            small_blind.money -= game_rules.SMALL_BLIND
            done = True
        except InsufficientMoneyError:
            self.remove_player(small_blind)
        except OutOfMoneyError:
            self.remove_player(small_blind)
        
        if len(self.players) == 1:
            self.game_over()
        elif not done:
            self._set_small_blind()

    def _set_big_blind(self) -> None:
        big_blind = self.players[self.big_blind_index]
        done = False
        
        # Try to remove the money
        try:
            big_blind.money -= game_rules.SMALL_BLIND
            done = True
        except InsufficientMoneyError:
            self.remove_player(big_blind)
        except OutOfMoneyError:
            self.remove_player(big_blind)
        
        if len(self.players) == 1:
            self.game_over()
        elif not done:
            self._set_small_blind()
    
    def _end_round(self, earnings: dict[Player, int]) -> None:
        for player, earning in earnings.items():
            player.money = player.money + earning
    
    def run(self) -> None:
        while len(self.players) >= 2:
            self.deck.shuffle()
            self.play_round()
            self.deck.reset()
        else:
            self.game_over()
    
    def game_over(self) -> None:
        print("[i] Game over!")
