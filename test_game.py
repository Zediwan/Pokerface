import unittest

from src.game.game import Game
from src.game.player import Player
from src.game import game_rules

class GameTestCase(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.player1 = Player("Alice")
        self.player2 = Player("Bob")
        self.player3 = Player("Charlie")
        self.game.add_player(self.player1)
        self.game.add_player(self.player2)
        self.game.add_player(self.player3)

        self.game.small_blind_index = 0

    def tearDown(self) -> None:
        print(self.player1)
        print(self.player2)
        print(self.player3)
        print("\n")

    def test_set_small_blind_valid(self):
        self.game.set_small_blind()
        self.assertEqual(self.player1.money, game_rules.STARTING_MONEY - game_rules.SMALL_BLIND)

    def test_set_small_blind_insufficient_money(self):
        self.player1._money = game_rules.SMALL_BLIND - 1
        self.game.set_small_blind()

        self.assertNotIn(self.player1, self.game.players)
        self.assertEqual(self.player2.money, game_rules.STARTING_MONEY - game_rules.SMALL_BLIND)

    def test_set_small_blind_insufficient_money_game_over(self):
        self.player1._money = game_rules.SMALL_BLIND - 1
        self.player2._money = game_rules.SMALL_BLIND - 1
        self.game.set_small_blind()

        self.assertNotIn(self.player1, self.game.players)
        self.assertNotIn(self.player2, self.game.players)
        self.assertEqual(self.player3.money, game_rules.STARTING_MONEY)
    
    def test_set_small_blind_end_of_list(self):
        self.game.small_blind_index = len(self.game.players) - 1
        self.game.set_small_blind()
        self.assertEqual(self.game.small_blind_index, 0)

if __name__ == '__main__':
    unittest.main()