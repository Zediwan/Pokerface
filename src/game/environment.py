from .player import Player
from .deck import Deck
from .card import Card
from . import game_rules

class Environment():
    min_players = 2
    
    @property 
    def table_cards(self) -> list[Card]:
        return self.the_flop + [self.turn_card] + [self.the_river]
    
    def __init__(self) -> None:
        self.deck: Deck = Deck()
        self.the_flop: list[Card] = []
        self.turn_card: Card = None
        self.the_river: Card = None

        self.small_blind: Player = None
        self.big_blind: Player = None
        self.current_player: Player =  None
        
        self.pot: int = 0
        self.current_bet: int = 0
        self.starting_score: int = 100
    
    # region player handling
    def add_player(self, player: Player) -> None:
        if self.small_blind is None:
            self.small_blind = player
            player.next_player = player
            player.prev_player = player
        elif self.big_blind is None:
            self.big_blind = player
            player.prev_player = self.small_blind
            player.next_player = self.small_blind
            self.small_blind.next_player = player
            self.small_blind.prev_player = player
        else:
            next_player = self.big_blind

            while next_player.next_player != self.small_blind:
                next_player = next_player.next_player
            
            next_player.next_player = player
            player.prev_player = next_player
            player.next_player = self.small_blind
            self.small_blind.prev_player = player
        player._money = self.starting_score
        print(f"[P] {player.name} added to the game")

        # Print order
        p = self.small_blind.next_player
        order = self.small_blind.name
        while p != self.small_blind:
            order += " -> " + p.name
            p = p.next_player
        print(f"[O] Current order: {order}")
    
    def remove_player(self, player: Player) -> None:
        if player == self.small_blind:
            self.small_blind = player.next_player
            self.big_blind = self.small_blind.next_player
        if player == self.big_blind:
            self.big_blind = player.prev_player
        
        player.prev_player.next_player = player.next_player
        player.next_player.prev_player = player.prev_player
    # endregion

    # region game
    def start_game(self) -> None:
        if self.small_blind is None or self.big_blind is None:
            raise ValueError("Not enough players to start game")
        
        self._reset()
        self._deal_cards()
        
        self._place_blinds()
        self.pre_flop_round()
        #self.deck.draw() # Burn a card
        #self.flop_round()
        #self.deck.draw() # Burn a card
        #self.turn_round()
        #self.deck.draw() # Burn a card
        #self.river_round()
        #self.deck.draw() # Burn a card
        #self.showdown_round()
        
        # Print players scores
        print(self._player_overview()) 
    
    def _reset(self) -> None:
        # Reset pot and bets
        self.pot = 0
        self.current_bet = 0

        # Reset cards
        self.deck.reset()
        self.the_flop = []
        self.turn_card = None
        self.the_river = None
        
        # Reset players
        player = self.small_blind
        player.cards = []
        while player != self.small_blind:
            player.cards = []
            player = player.next_player
        self.current_player = self.small_blind
    
    def _deal_cards(self) -> None:
        for _ in range(2):
            self.current_player.deal_card(self.deck.draw())
            self.current_player = self.current_player.next_player
            while self.current_player != self.small_blind:
                self.current_player.deal_card(self.deck.draw())
                self.current_player = self.current_player.next_player
    
    def _place_blinds(self) -> None:
        sb_paid = False
        bb_paid = False

        # Small blind
        while not sb_paid:
            try:
                sb_paid = self.small_blind.pay_small_blind()
                print(f"[SB] {self.small_blind.name} pays the small blind ({game_rules.SMALL_BLIND})")
            except ValueError:
                print(f"[!] {self.small_blind.name} does not have enough money for small blind and is therefore kicked from the game. ({self.small_blind.money})")
                self.remove_player(self.small_blind)
        self.pot += game_rules.SMALL_BLIND
        
        # Big blind
        while not bb_paid:
            try:
                bb_paid = self.big_blind.pay_big_blind()
                print(f"[BB] {self.big_blind.name} pays the big blind ({game_rules.BIG_BLIND})")
            except ValueError:
                print(f"[!] {self.big_blind.name} does not have enough money for big blind and is therefore kicked from the game. ({self.big_blind.money})")
                self.remove_player(self.big_blind)
        self.pot += game_rules.BIG_BLIND
        
        self.current_bet = game_rules.BIG_BLIND
        self.current_player = self.big_blind.next_player
    
    # region game phases
    def pre_flop_round(self) -> None:
        times_raised = 0

        first_player = self.small_blind
        self.current_player = first_player

        move = first_player.make_move()
        if move:
            # Raise or Check
            self.pot += move
            self.current_bet = move
        # Go to the next player
        self.current_player = self.current_player.next_player

        # Repeat until first player to change something has been reached
        while self.current_player != first_player:
            move = self.current_player.make_move(
                prev_raise = self.current_bet - self.current_player.bet_this_round, 
                can_re_raise = times_raised < game_rules.MAX_TIMES_RAISABLE_PER_ROUND
                )

            if move is not None:
                # Raise or Check
                self.pot += move
                self.current_bet = move
            else:
                self.remove_player(self.current_player)

            # Go to the next player
            self.current_player = self.current_player.next_player

        self._reset_player_round_bets()
    
    def flop_round(self) -> None:
        pass
    
    def turn_round(self) -> None:
        pass
    
    def river_round(self) -> None:
        pass
    
    def showdown_round(self) -> None:
        pass
    # endregion
    
    # region helpers
    def _reset_player_round_bets(self) -> None:
        p = self.small_blind
        p.bet_this_round = 0
        p = p.next_player
        
        while p != self.small_blind:
            p.bet_this_round = 0
            p = p.next_player    
    # endregion

    # endregion

    # region information
    def _player_overview(self) -> str:
        overview = "\n"
        overview += "-------------- Overview --------------\n"
        p = self.small_blind
        overview += p.__str__() + "\n"
        p = p.next_player
        while p != self.small_blind:
            overview += p.__str__() + "\n"
            p = p.next_player
        return overview
    # endregion
