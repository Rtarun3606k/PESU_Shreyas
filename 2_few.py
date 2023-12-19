import tkinter as tk
from tkinter import simpledialog, messagebox
import random

class SnakeAndLaddersGame:
    def __init__(self, root):
        # Initialize the SnakeAndLaddersGame instance
        self.root = root
        self.root.title("Snake & Ladders")
        self.root.resizable(width=False, height=False)

        # Get player name(s)
        self.players = self.get_player_names()

        # Set up the game board
        self.board_size = 10
        self.create_board()

        # Initialize player positions, moves, and colors
        self.player_pos = [1] * len(self.players)
        self.player_moves = [0] * len(self.players)
        self.player_colors = self.generate_player_colors(len(self.players))

        # Define snake and ladder positions on the board
        self.snakes = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
        self.ladders = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}

        # Draw the initial game board
        self.draw_board()

    def get_player_names(self):
        # Prompt the user to enter the number of players
        num_players = simpledialog.askinteger("Number of Players", "Enter the number of players:", initialvalue=1)
        players = []
        # Prompt for each player's name
        for i in range(num_players):
            player_name = simpledialog.askstring("Player Name", f"Enter the name for Player {i + 1}:")
            players.append(player_name if player_name else f"Player {i + 1}")
        return players

    def generate_player_colors(self, num_players):
        # Generate a list of random colors for each player
        colors = ["red", "green", "blue", "orange", "purple", "brown", "pink", "gray", "cyan", "magenta"]
        return random.sample(colors, num_players)

    def create_board(self):
        # Create the Tkinter canvas for the game board
        self.canvas = tk.Canvas(self.root, width=600, height=600, bg='white')
        self.canvas.pack()

    def draw_board(self):
        # Draw the game board on the canvas
        cell_size = 60
        for row in range(self.board_size):
            for col in range(self.board_size):
                x0, y0 = col * cell_size, (self.board_size - 1 - row) * cell_size
                x1, y1 = x0 + cell_size, y0 + cell_size
                # Draw the cell rectangle
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=self.get_cell_color(row, col), outline='black')
                # Draw the cell number in the center
                self.canvas.create_text(x0 + cell_size // 2, y0 + cell_size // 2,
                                        text=str(row * self.board_size + col + 1), fill='black', font=('Arial', 12))

        # Draw initial player positions
        self.draw_players()

    def get_cell_color(self, row, col):
        # Determine the color of the cell based on snakes, ladders, and cell position
        cell_number = row * self.board_size + col + 1
        if cell_number in self.snakes:
            return 'red'
        elif cell_number in self.ladders:
            return 'green'
        elif (row + col) % 2 == 0:
            return 'lightgray'
        else:
            return 'white'

    def roll_dice(self):
        # Simulate rolling a six-sided die
        return random.randint(1, 6)

    def move_player(self, player_index, steps):
        # Clear previous player marks
        self.clear_player_marks()
        
        # Move the player on the board based on the dice roll
        self.player_pos[player_index] += steps
        self.player_moves[player_index] += 1

        # Check for snakes and ladders and update player position
        if self.player_pos[player_index] in self.snakes:
            self.player_pos[player_index] = self.snakes[self.player_pos[player_index]]
        elif self.player_pos[player_index] in self.ladders:
            self.player_pos[player_index] = self.ladders[self.player_pos[player_index]]

        # Ensure the player's position is within the valid range
        self.player_pos[player_index] = max(1, min(self.player_pos[player_index], self.board_size**2))

        # Update the player positions on the canvas
        self.draw_players()

        # Check if the player has reached or passed the last cell
        if self.player_pos[player_index] >= self.board_size**2:
            messagebox.showinfo("Game Over", f"Congratulations, {self.players[player_index]}! You won in {self.player_moves[player_index]} moves.")
            self.reset_game()

    def clear_player_marks(self):
        # Clear previous player marks on the canvas
        self.canvas.delete('players')

    def draw_players(self):
        # Draw the players' positions on the canvas
        cell_size = 60
        for i, pos in enumerate(self.player_pos):
            row = (pos - 1) // self.board_size
            col = (pos - 1) % self.board_size
            x, y = col * cell_size + cell_size // 2, (self.board_size - 1 - row) * cell_size + cell_size // 2  # Adjusted y coordinate
            # Draw an oval representing the player with the assigned color
            self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill=self.player_colors[i], tags='players')

    def reset_game(self):
        # Reset the game state to the initial state
        self.player_pos = [1] * len(self.players)
        self.player_moves = [0] * len(self.players)
        # Redraw the players on the canvas
        self.draw_players()

    def play_turn(self):
        # Play a turn for each player
        for i in range(len(self.players)):
            # Roll the dice
            steps = self.roll_dice()
            # Display dice roll information
            messagebox.showinfo("Dice Roll", f"{self.players[i]}, you rolled a {steps}.")
            # Move the player based on the dice roll
            self.move_player(i, steps)


if __name__ == "__main__":
    # Create the Tkinter root window
    root = tk.Tk()
    # Create an instance of the SnakeAndLaddersGame
    game = SnakeAndLaddersGame(root)

    # Define a function for playing a turn
    def play_turn():
        game.play_turn()

    # Create a button for rolling the dice
    play_button = tk.Button(root, text="Roll Dice", command=play_turn)
    play_button.pack()

    # Create a button for resetting the game
    reset_button = tk.Button(root, text="Reset Game", command=game.reset_game)
    reset_button.pack()

    # Start the Tkinter event loop
    root.mainloop()
