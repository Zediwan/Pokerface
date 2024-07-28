from src.game.environment import Environment
from src.game.player import Player

if __name__ == "__main__":
    env = Environment()
    names = ["Jeremy", "Jan", "Laurin", "Lou"]
    players = [Player(name) for name in names]
    for player in players:
        env.add_player(player)
    env.start_game()