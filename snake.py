import tkinter as tk
from tkinter import messagebox
from tkinter import font
import random

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")
        self.root.configure(bg='#2c3e50')
        self.root.resizable(False, False)
        
        # Game parameters
        self.GRID_WIDTH = 20
        self.GRID_HEIGHT = 20
        self.CELL_SIZE = 20
        self.GAME_SPEED = 100  # milliseconds
        
        # Game state
        self.snake = [(10, 10), (9, 10), (8, 10)]  # Head is first
        self.food = self.spawn_food()
        self.direction = (1, 0)  # (dx, dy) - moving right
        self.next_direction = (1, 0)
        self.score = 0
        self.game_over = False
        
        # Set up UI
        self.setup_ui()
        
        # Bind keys
        self.root.bind('<KeyPress>', self.on_key_press)
        
        # Start game loop
        self.game_loop()
    
    def setup_ui(self):
        """Set up the game interface."""
        # Title frame
        title_frame = tk.Frame(self.root, bg='#2c3e50')
        title_frame.pack(pady=10)
        
        title_font = font.Font(family="Helvetica", size=20, weight="bold")
        title_label = tk.Label(
            title_frame,
            text="Snake Game",
            font=title_font,
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        title_label.pack()
        
        # Score frame
        score_frame = tk.Frame(self.root, bg='#2c3e50')
        score_frame.pack(pady=5)
        
        score_font = font.Font(family="Helvetica", size=14)
        self.score_label = tk.Label(
            score_frame,
            text="Score: 0",
            font=score_font,
            bg='#2c3e50',
            fg='#2ecc71'
        )
        self.score_label.pack()
        
        # Game canvas
        canvas_frame = tk.Frame(self.root, bg='#34495e')
        canvas_frame.pack(pady=10, padx=10)
        
        self.canvas = tk.Canvas(
            canvas_frame,
            width=self.GRID_WIDTH * self.CELL_SIZE,
            height=self.GRID_HEIGHT * self.CELL_SIZE,
            bg='#FFFFFF',
            highlightthickness=2,
            highlightbackground='#34495e'
        )
        self.canvas.pack()
        
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
            padx=15,
            pady=8,
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
            padx=15,
            pady=8,
            activebackground='#c0392b'
        )
        quit_btn.pack(side=tk.LEFT, padx=5)
        
        # Instructions frame
        instr_frame = tk.Frame(self.root, bg='#2c3e50')
        instr_frame.pack(pady=5)
        
        instr_font = font.Font(family="Helvetica", size=9)
        instr_label = tk.Label(
            instr_frame,
            text="Use WASD to move - Eat food to grow and gain points!",
            font=instr_font,
            bg='#2c3e50',
            fg='#95a5a6'
        )
        instr_label.pack()
    
    def spawn_food(self):
        """Spawn food at a random location not occupied by snake."""
        while True:
            x = random.randint(0, self.GRID_WIDTH - 1)
            y = random.randint(0, self.GRID_HEIGHT - 1)
            if (x, y) not in self.snake:
                return (x, y)
    
    def on_key_press(self, event):
        """Handle keyboard input."""
        if self.game_over:
            return
        
        key = event.keysym.lower()
        
        if key == 'w':
            self.next_direction = (0, -1)
        elif key == 's':
            self.next_direction = (0, 1)
        elif key == 'a':
            self.next_direction = (-1, 0)
        elif key == 'd':
            self.next_direction = (1, 0)
    
    def update_game(self):
        """Update game state."""
        if self.game_over:
            return
        
        # Update direction
        self.direction = self.next_direction
        
        # Calculate new head position
        head_x, head_y = self.snake[0]
        new_x = head_x + self.direction[0]
        new_y = head_y + self.direction[1]
        
        # Check wall collision
        if new_x < 0 or new_x >= self.GRID_WIDTH or new_y < 0 or new_y >= self.GRID_HEIGHT:
            self.end_game()
            return
        
        # Check self collision
        if (new_x, new_y) in self.snake:
            self.end_game()
            return
        
        # Move snake
        self.snake.insert(0, (new_x, new_y))
        
        # Check food collision
        if (new_x, new_y) == self.food:
            self.score += 10
            self.food = self.spawn_food()
        else:
            self.snake.pop()
        
        self.draw_game()
    
    def draw_game(self):
        """Draw the game on canvas."""
        self.canvas.delete("all")
        
        # Draw grid (optional)
        grid_color = '#2a3f5f'
        for i in range(0, self.GRID_WIDTH * self.CELL_SIZE, self.CELL_SIZE):
            self.canvas.create_line(i, 0, i, self.GRID_HEIGHT * self.CELL_SIZE, fill=grid_color, width=0)
        for i in range(0, self.GRID_HEIGHT * self.CELL_SIZE, self.CELL_SIZE):
            self.canvas.create_line(0, i, self.GRID_WIDTH * self.CELL_SIZE, i, fill=grid_color, width=0)
        
        # Draw snake
        for i, (x, y) in enumerate(self.snake):
            # Head is brighter
            if i == 0:
                color = '#2ecc71'
            else:
                color = '#27ae60'
            
            x1 = x * self.CELL_SIZE + 1
            y1 = y * self.CELL_SIZE + 1
            x2 = x1 + self.CELL_SIZE - 2
            y2 = y1 + self.CELL_SIZE - 2
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)
        
        # Draw food
        x, y = self.food
        x1 = x * self.CELL_SIZE + 1
        y1 = y * self.CELL_SIZE + 1
        x2 = x1 + self.CELL_SIZE - 2
        y2 = y1 + self.CELL_SIZE - 2
        self.canvas.create_oval(x1, y1, x2, y2, fill='#1a252f', outline='#1a252f')
        
        # Update score label
        self.score_label.config(text=f"Score: {self.score}")
    
    def game_loop(self):
        """Main game loop."""
        self.update_game()
        if not self.game_over:
            self.root.after(self.GAME_SPEED, self.game_loop)
    
    def end_game(self):
        """Handle game over."""
        self.game_over = True
        messagebox.showinfo("Game Over", f"Game Over! Final Score: {self.score}")
        self.reset_game()
    
    def reset_game(self):
        """Reset the game to initial state."""
        self.snake = [(10, 10), (9, 10), (8, 10)]
        self.food = self.spawn_food()
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.score = 0
        self.game_over = False
        self.draw_game()


if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
