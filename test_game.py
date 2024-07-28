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

    def tearDown(self) -> None:
        print(self.player1)
        print(self.player2)
        print(self.player3)
        print("\n")

    # region set_small_blind
    def test_set_small_blind_valid(self):
        """
        Test case to verify if the small blind is set correctly.

        This test sets the small blind in the game and checks if the player's money is updated correctly.
        It asserts that the player's money is equal to the starting money minus the small blind amount.

        """
        self.game._set_small_blind()
        self.assertEqual(self.player1.money, game_rules.STARTING_MONEY - game_rules.SMALL_BLIND)

    def test_set_small_blind_insufficient_money(self):
        """
        Test case to verify the behavior when a player has insufficient money to place the small blind.

        This test sets the money of player1 to be less than the small blind amount. Then, it calls the
        `set_small_blind` method of the game. The test checks that player1 is not included in the list
        of players and that player2's money is reduced by the small blind amount.

        This test ensures that the game correctly handles the scenario when a player does not have enough
        money to place the small blind.

        """
        self.player1._money = game_rules.SMALL_BLIND - 1
        self.game._set_small_blind()

        self.assertNotIn(self.player1, self.game.players)
        self.assertEqual(self.player2.money, game_rules.STARTING_MONEY - game_rules.SMALL_BLIND)

    def test_set_small_blind_insufficient_money_game_over(self):
        """
        Test case to verify that if a player has insufficient money to pay the small blind,
        they are removed from the game and their money is reset to the starting amount.
        """
        self.player1._money = game_rules.SMALL_BLIND - 1
        self.player2._money = game_rules.SMALL_BLIND - 1
        self.game._set_small_blind()

        self.assertNotIn(self.player1, self.game.players)
        self.assertNotIn(self.player2, self.game.players)
        self.assertEqual(self.player3.money, game_rules.STARTING_MONEY)
    # endregion

if __name__ == '__main__':
    unittest.main()