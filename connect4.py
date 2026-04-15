import tkinter as tk
from tkinter import messagebox
from tkinter import font
import numpy as np

class Connect4Game:
    def __init__(self, root):
        self.root = root
        self.root.title("Connect 4")
        self.root.configure(bg='#2c3e50')
        
        # Game parameters
        self.ROWS = 6
        self.COLS = 7
        self.PLAYER1 = 1
        self.PLAYER2 = 2
        self.EMPTY = 0
        
        # Initialize game board
        self.board = np.zeros((self.ROWS, self.COLS), dtype=int)
        self.current_player = self.PLAYER1
        
        # Set up UI
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the game interface."""
        # Title frame
        title_frame = tk.Frame(self.root, bg='#2c3e50')
        title_frame.pack(pady=10)
        
        title_font = font.Font(family="Helvetica", size=20, weight="bold")
        title_label = tk.Label(
            title_frame,
            text="Connect 4",
            font=title_font,
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        title_label.pack()
        
        # Game info frame
        info_frame = tk.Frame(self.root, bg='#2c3e50')
        info_frame.pack(pady=10)
        
        info_font = font.Font(family="Helvetica", size=12)
        self.info_label = tk.Label(
            info_frame,
            text="Player 1 (Red) - Your Turn",
            font=info_font,
            bg='#2c3e50',
            fg='#e74c3c'
        )
        self.info_label.pack()
        
        # Game board frame
        board_frame = tk.Frame(self.root, bg='#34495e', relief=tk.RAISED, bd=3)
        board_frame.pack(pady=20)
        
        # Create buttons for each column
        self.column_buttons = []
        for col in range(self.COLS):
            btn = tk.Button(
                board_frame,
                text=f"↓",
                font=font.Font(family="Helvetica", size=16, weight="bold"),
                width=6,
                height=2,
                command=lambda c=col: self.drop_piece(c),
                bg='#7f8c8d',
                fg='#ecf0f1',
                activebackground='#95a5a6'
            )
            btn.grid(row=0, column=col, padx=2, pady=2)
            self.column_buttons.append(btn)
        
        # Create grid of circles for the board display
        self.cell_buttons = []
        for row in range(self.ROWS):
            row_buttons = []
            for col in range(self.COLS):
                btn = tk.Button(
                    board_frame,
                    width=6,
                    height=2,
                    state=tk.DISABLED,
                    bg='#3498db',
                    activebackground='#3498db'
                )
                btn.grid(row=row+1, column=col, padx=2, pady=2)
                row_buttons.append(btn)
            self.cell_buttons.append(row_buttons)
        
        # Control buttons frame
        control_frame = tk.Frame(self.root, bg='#2c3e50')
        control_frame.pack(pady=10)
        
        reset_btn = tk.Button(
            control_frame,
            text="New Game",
            command=self.reset_game,
            font=font.Font(family="Helvetica", size=11),
            bg='#27ae60',
            fg='#ecf0f1',
            padx=20,
            pady=10,
            activebackground='#229954'
        )
        reset_btn.pack(side=tk.LEFT, padx=5)
        
        quit_btn = tk.Button(
            control_frame,
            text="Quit",
            command=self.root.quit,
            font=font.Font(family="Helvetica", size=11),
            bg='#e74c3c',
            fg='#ecf0f1',
            padx=20,
            pady=10,
            activebackground='#c0392b'
        )
        quit_btn.pack(side=tk.LEFT, padx=5)
        
        # Update display
        self.update_display()
    
    def drop_piece(self, col):
        """Drop a piece in the specified column."""
        # Find the lowest empty row in the column
        for row in range(self.ROWS - 1, -1, -1):
            if self.board[row, col] == self.EMPTY:
                self.board[row, col] = self.current_player
                self.update_display()
                
                # Check for win
                if self.check_win(row, col):
                    player_name = "Player 1 (Red)" if self.current_player == self.PLAYER1 else "Player 2 (Yellow)"
                    messagebox.showinfo("Game Over", f"{player_name} wins!")
                    self.reset_game()
                    return
                
                # Check for draw
                if np.all(self.board[0, :] != self.EMPTY):
                    messagebox.showinfo("Game Over", "It's a draw!")
                    self.reset_game()
                    return
                
                # Switch player
                self.current_player = self.PLAYER2 if self.current_player == self.PLAYER1 else self.PLAYER1
                self.update_display()
                return
        
        # Column is full
        messagebox.showwarning("Invalid Move", "This column is full!")
    
    def check_win(self, row, col):
        """Check if the current player has won."""
        player = self.current_player
        
        # Check horizontal
        count = 1
        # Check left
        c = col - 1
        while c >= 0 and self.board[row, c] == player:
            count += 1
            c -= 1
        # Check right
        c = col + 1
        while c < self.COLS and self.board[row, c] == player:
            count += 1
            c += 1
        if count >= 4:
            return True
        
        # Check vertical
        count = 1
        # Check down
        r = row + 1
        while r < self.ROWS and self.board[r, col] == player:
            count += 1
            r += 1
        # Check up
        r = row - 1
        while r >= 0 and self.board[r, col] == player:
            count += 1
            r -= 1
        if count >= 4:
            return True
        
        # Check diagonal (top-left to bottom-right)
        count = 1
        # Check down-right
        r, c = row + 1, col + 1
        while r < self.ROWS and c < self.COLS and self.board[r, c] == player:
            count += 1
            r += 1
            c += 1
        # Check up-left
        r, c = row - 1, col + 1
        while r >= 0 and c < self.COLS and self.board[r, c] == player:
            count += 1
            r -= 1
            c += 1
        if count >= 4:
            return True
        
        # Check diagonal (bottom-left to top-right)
        count = 1
        # Check down-left
        r, c = row + 1, col - 1
        while r < self.ROWS and c >= 0 and self.board[r, c] == player:
            count += 1
            r += 1
            c -= 1
        # Check up-right
        r, c = row - 1, col + 1
        while r >= 0 and c < self.COLS and self.board[r, c] == player:
            count += 1
            r -= 1
            c += 1
        if count >= 4:
            return True
        
        return False
    
    def update_display(self):
        """Update the game board display and info label."""
        # Update info label
        player_name = "Player 1 (Red)" if self.current_player == self.PLAYER1 else "Player 2 (Yellow)"
        player_color = "#e74c3c" if self.current_player == self.PLAYER1 else "#f39c12"
        self.info_label.config(text=f"{player_name} - Your Turn", fg=player_color)
        
        # Update board display
        for row in range(self.ROWS):
            for col in range(self.COLS):
                if self.board[row, col] == self.EMPTY:
                    self.cell_buttons[row][col].config(bg='#3498db')
                elif self.board[row, col] == self.PLAYER1:
                    self.cell_buttons[row][col].config(bg='#e74c3c')
                else:  # PLAYER2
                    self.cell_buttons[row][col].config(bg='#f39c12')
    
    def reset_game(self):
        """Reset the game to initial state."""
        self.board = np.zeros((self.ROWS, self.COLS), dtype=int)
        if self.current_player == self.PLAYER1:
            self.current_player = self.PLAYER1
        self.update_display()


if __name__ == "__main__":
    root = tk.Tk()
    game = Connect4Game(root)
    root.mainloop()
