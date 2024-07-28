from . import game_rules
from .card import Card

class OutOfMoneyError(Exception):
    pass

class InsufficientMoneyError(Exception):
    pass

class Player():    
    def __init__(self, name: str = None) -> None:
        # if not name:
        #     name = input("Enter player name: ")
        self.name = name

        self.cards: list[Card] = []

        self._money = 0
        self.bet_this_round = 0
        self.bet_this_game = 0
        
        # Stats
        self.money_earned = 0
        self.money_lost = 0
        self.times_folded = 0
        self.times_raised = 0
        self.times_checked = 0
        self.times_called = 0

        self.prev_player: Player = None
        self.next_player: Player = None
        
        print(f"[P] Player created: " + self.name)
    
    @property
    def money(self) -> int:
        return self._money
    
    @money.setter
    def money(self, new_balance: int) -> int:
        if new_balance < 0:
            raise InsufficientMoneyError("[E] Player does not have enough money.")
        if new_balance == 0:
            raise OutOfMoneyError(f"[!] {self.name} has no money left")
        if new_balance > self._money:
            money_made = new_balance - self._money
            print(f"[+$] {self.name} gains {money_made}")
            self.money_earned += money_made
        elif new_balance < self._money:
            money_spent = self._money - new_balance
            print(f"[-$] {self.name} spends {money_spent}")
            self.money_lost += money_spent
            self.bet_this_game += money_spent
            self.bet_this_round += money_spent

        self._money = new_balance
    
    @property
    def playing(self) -> bool:
        return len(self.cards) > 0
    
    def deal_card(self, card: Card) -> None:
        if len(self.cards) >= game_rules.MAX_POSSIBLE_CARDS_ON_HAND:
            raise ValueError(f"[E] Cannot have more than {game_rules.MAX_POSSIBLE_CARDS_ON_HAND} cards.")

        self.cards.append(card)

        print("[D] " + self.name + " drew " + card.__str__())
    
    def make_move(self, prev_raise: int = 0, can_re_raise: bool = True) -> int:
        if prev_raise < 0:
            raise ValueError("[E] Previous raise cannot be smaller than 0!")
        # Decide move
        print(f"[M] {self.name}'s turn")
        
        can_re_raise = can_re_raise and self.money >= prev_raise + game_rules.BIG_BLIND

        if prev_raise > 0:
            print(f"[i] Amount needed to Call {prev_raise} ({self._money} left)")
            if can_re_raise:
                action = input(f"[?] CALL / RAISE / FOLD")
            else:
                action = input(f"[?] CALL / FOLD")
        else:
            action = input(f"[?] CHECK / RAISE / FOLD")

        match action:
            case "CALL":
                return self._call(previous_raise=prev_raise)
            case "RAISE":
                return self._raise(previous_raise=prev_raise)
            case "CHECK":
                return self._check()
            case "FOLD":
                return self._fold()
            case _:
                print("[E] Invalid action")
                self.make_move(prev_raise=prev_raise, can_re_raise=can_re_raise)
    
    def _raise(self, previous_raise: int = 0) -> int:
        self.times_raised += 1

        valid = False
        while not valid:
            amount_to_raise = input(f"[?] How much do you want to raise (at least {game_rules.MIN_BET})? ({self._money} left)")
            if amount_to_raise < 0:
                print("[E] Amount needs to be positive integer")
            elif amount_to_raise + previous_raise > self._money:
                print("[E] Player does not have enough money.")
            elif amount_to_raise < game_rules.MIN_BET:
                print(f"[E] Raised amount needs to be at least the min bet {game_rules.MIN_BET}.")
            else:
                valid = True
        
        self.money = self.money - amount_to_raise - previous_raise
        print(f"[M] {self.name} raises for {amount_to_raise}. ({self._money} left)")

        return amount_to_raise
    
    def _call(self, previous_raise: int) -> int:
        self.times_called += 1

        if previous_raise > self._money:
            print("[E] Player does not have enough money.")
            return self._fold()
        
        self.money = self.money - previous_raise
        print(f"[M] {self.name} calls {previous_raise}. ({self._money} left)")
        
        return previous_raise
    
    def _fold(self) -> None:
        self.times_folded += 1

        print(f"[M] {self.name} folds his cards")
        return None
    
    def _check(self) -> int:
        self.times_checked += 1
        print(f"[M] {self.name} checks.")
        return 0
    
    def pay_big_blind(self) -> bool:
        self.money = self.money - game_rules.BIG_BLIND
            
    def pay_small_blind(self) -> bool:
        self.money = self.money - game_rules.SMALL_BLIND
    
    def __str__(self) -> str:
        string = "--------------------------------------\n"
        string += f"|Name: {self.name}\n"
        string += f"|Money: {self._money}\n"
        string += "|Cards: "
        for card in self.cards:
            string += card.__str__()
        string += "\n"
        string += "--------------------------------------"

        return string
