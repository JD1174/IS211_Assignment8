import random
import argparse
import time

class Player:
    def __init__(self, name):
        """Initialize a Player with a name and a score of 0."""
        self.name = name
        self.score = 0

    def reset_score(self):
        """Reset the player's score to 0 (used when restarting the game)."""
        self.score = 0

    def __str__(self):
        """String representation of a player's current state."""
        return f"{self.name}: {self.score} points"

class HumanPlayer(Player):
    """A human player inherits from the base Player class."""
    pass

class ComputerPlayer(Player):
    """A computer player inherits from the base Player class and uses a strategy to decide actions."""

    def decide(self, turn_total):
        """Computer strategy: Hold at the lesser of 25 or 100 minus current score."""
        if turn_total >= min(25, 100 - self.score):
            return 'h'  # Hold
        return 'r'  # Roll again

class PlayerFactory:
    """Factory class to create human or computer players based on input."""

    @staticmethod
    def create_player(player_type, name):
        """Creates either a HumanPlayer or ComputerPlayer."""
        if player_type == 'human':
            return HumanPlayer(name)
        elif player_type == 'computer':
            return ComputerPlayer(name)
        else:
            raise ValueError("Unknown player type: must be 'human' or 'computer'")

class Die:
    def roll(self):
        """Roll the die and return a random integer between 1 and 6."""
        return random.randint(1, 6)

class PigGame:
    def __init__(self, player1_type, player2_type):
        """Initialize the game with two players."""
        self.players = [
            PlayerFactory.create_player(player1_type, "Player 1"),
            PlayerFactory.create_player(player2_type, "Player 2")
        ]
        self.die = Die()
        self.current_player_index = 0

    def switch_player(self):
        """Switch to the next player after the current turn."""
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def play_turn(self):
        """Allow the current player to roll or hold, implementing the game rules."""
        current_player = self.players[self.current_player_index]
        turn_total = 0

        while True:
            roll = self.die.roll()
            print(f"\n{current_player.name} rolled a {roll}")

            if roll == 1:
                print(f"{current_player.name} scores nothing this turn.")
                break

            turn_total += roll
            print(f"Turn total: {turn_total}, {current_player}")

            # If it's a computer player's turn, use its strategy to decide
            if isinstance(current_player, ComputerPlayer):
                decision = current_player.decide(turn_total)
                print(f"{current_player.name} decides to {'hold' if decision == 'h' else 'roll again'}.")
            else:
                # Otherwise, prompt the human player for input
                decision = input("Roll again (r), hold (h), or quit (q/quit/exit)? ").strip().lower()
                if decision in ['q', 'quit', 'exit']:
                    print("Thanks for playing! Exiting the game.")
                    exit()

            if decision == 'h':
                current_player.score += turn_total
                print(f"{current_player.name} holds. Total score: {current_player.score}")
                break

        self.switch_player()

    def is_game_over(self):
        """Check if any player has reached a score of 100 or more."""
        return any(player.score >= 100 for player in self.players)

    def play_game(self):
        """Main game loop: play turns until a player reaches the winning score."""
        print("\nWelcome to the game of Pig!\n")
        while not self.is_game_over():
            self.play_turn()

        winner = max(self.players, key=lambda player: player.score)
        print(f"\n{winner.name} wins with {winner.score} points!")
        print("\nFinal Scores:")
        for player in self.players:
            print(player)

    def reset_game(self):
        """Reset the game state to play another round, resetting player scores and turns."""
        for player in self.players:
            player.reset_score()
        self.current_player_index = 0

class TimedGameProxy:
    """Proxy class for the game that introduces a timed component."""

    def __init__(self, game, time_limit=60):
        """Initialize the proxy with a reference to the game and a time limit (in seconds)."""
        self.game = game
        self.time_limit = time_limit

    def play_game(self):
        """Main game loop, but with a time limit."""
        start_time = time.time()
        print("\nStarting timed game of Pig!")
        
        while not self.game.is_game_over():
            current_time = time.time()
            elapsed_time = current_time - start_time
            
            # Check time before allowing the current player to take their turn
            if elapsed_time > self.time_limit:
                print(f"\nTime's up! The game lasted {int(elapsed_time)} seconds.")
                break

            self.game.play_turn()

        # Even if time runs out, determine the winner by score
        winner = max(self.game.players, key=lambda player: player.score)
        print(f"\n{winner.name} wins with {winner.score} points!")
        print("\nFinal Scores:")
        for player in self.game.players:
            print(player)

def main(player1_type, player2_type, timed):
    """Main entry point for running the game with player types and timed option."""
    game = PigGame(player1_type, player2_type)

    if timed:
        proxy = TimedGameProxy(game)
        proxy.play_game()
    else:
        game.play_game()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Play the game of Pig.")
    parser.add_argument("--player1", type=str, choices=["human", "computer"], default="human", help="Type of player 1 (human or computer)")
    parser.add_argument("--player2", type=str, choices=["human", "computer"], default="computer", help="Type of player 2 (human or computer)")
    parser.add_argument("--timed", action="store_true", help="Play a timed version of the game")

    args = parser.parse_args()
    main(args.player1, args.player2, args.timed)