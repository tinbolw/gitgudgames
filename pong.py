import tkinter as tk
from tkinter import font
import random
import math

class PongGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Pong Game")
        self.root.configure(bg='#2c3e50')
        self.root.resizable(False, False)
        
        # Game parameters
        self.CANVAS_WIDTH = 800
        self.CANVAS_HEIGHT = 400
        self.PADDLE_WIDTH = 10
        self.PADDLE_HEIGHT = 80
        self.BALL_SIZE = 8
        self.PADDLE_SPEED = 6
        self.GAME_SPEED = 30  # milliseconds
        
        # Game state
        self.left_paddle_y = self.CANVAS_HEIGHT / 2
        self.right_paddle_y = self.CANVAS_HEIGHT / 2
        self.ball_x = self.CANVAS_WIDTH / 2
        self.ball_y = self.CANVAS_HEIGHT / 2
        self.ball_dx = 5
        self.ball_dy = 5
        self.left_score = 0
        self.right_score = 0
        self.game_over = False
        
        # Key states
        self.left_paddle_up = False
        self.left_paddle_down = False
        self.right_paddle_up = False
        self.right_paddle_down = False
        
        # Set up UI
        self.setup_ui()
        
        # Bind keys
        self.root.bind('<KeyPress>', self.on_key_press)
        self.root.bind('<KeyRelease>', self.on_key_release)
        
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
            text="Pong",
            font=title_font,
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        title_label.pack()
        
        # Score frame
        score_frame = tk.Frame(self.root, bg='#2c3e50')
        score_frame.pack(pady=5)
        
        score_font = font.Font(family="Helvetica", size=16, weight="bold")
        self.score_label = tk.Label(
            score_frame,
            text="Player 1: 0  |  Player 2: 0",
            font=score_font,
            bg='#2c3e50',
            fg='#3498db'
        )
        self.score_label.pack()
        
        # Game canvas
        canvas_frame = tk.Frame(self.root, bg='#34495e')
        canvas_frame.pack(pady=10, padx=10)
        
        self.canvas = tk.Canvas(
            canvas_frame,
            width=self.CANVAS_WIDTH,
            height=self.CANVAS_HEIGHT,
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
            text="P1: W/S keys  |  P2: Up/Down arrows  |  First to 11 wins!",
            font=instr_font,
            bg='#2c3e50',
            fg='#95a5a6'
        )
        instr_label.pack()
    
    def on_key_press(self, event):
        """Handle key press."""
        key = event.keysym.lower()
        if self.right_paddle_y - self.PADDLE_HEIGHT >= self.CANVAS_HEIGHT:
            return
        if key == 'w':
            self.left_paddle_up = True
        elif key == 's':
            self.left_paddle_down = True
        elif key == 'up':
            self.right_paddle_up = True
        elif key == 'down':
            self.right_paddle_down = True
    
    def on_key_release(self, event):
        """Handle key release."""
        key = event.keysym.lower()
        
        if key == 'w':
            self.left_paddle_up = False
        elif key == 's':
            self.left_paddle_down = False
        elif key == 'up':
            self.right_paddle_up = False
        elif key == 'down':
            self.right_paddle_down = False
    
    def update_paddles(self):
        """Update paddle positions."""
        left_too_high = self.left_paddle_y - self.PADDLE_HEIGHT / 2 <= 0
        left_too_low = self.left_paddle_y + self.PADDLE_HEIGHT / 2 >= self.CANVAS_HEIGHT
        right_too_high = self.right_paddle_y - self.PADDLE_HEIGHT / 2 <= 0
        right_too_low = self.right_paddle_y + self.PADDLE_HEIGHT / 2 >= self.CANVAS_HEIGHT
        # Left paddle
        # Left paddle
        if self.left_paddle_up and not left_too_high:
            self.left_paddle_y -= self.PADDLE_SPEED
        if self.left_paddle_down and not left_too_low:
            self.left_paddle_y += self.PADDLE_SPEED
        
        # Right paddle
        if self.right_paddle_up and not right_too_high:
            self.right_paddle_y -= self.PADDLE_SPEED
        if self.right_paddle_down and not right_too_low:
            self.right_paddle_y += self.PADDLE_SPEED
    
    def update_ball(self):
        """Update ball position and check collisions."""
        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy
        
        # Top and bottom wall collision
        if self.ball_y - self.BALL_SIZE <= 0 or self.ball_y + self.BALL_SIZE >= self.CANVAS_HEIGHT:
            self.ball_dy = -self.ball_dy
            self.ball_y = max(self.BALL_SIZE, min(self.CANVAS_HEIGHT - self.BALL_SIZE, self.ball_y))
        
        # Left paddle collision
        if (self.ball_x - self.BALL_SIZE <= self.PADDLE_WIDTH and
            self.left_paddle_y - self.PADDLE_HEIGHT / 2 <= self.ball_y <= self.left_paddle_y + self.PADDLE_HEIGHT / 2):
            self.ball_dx = -self.ball_dx
            self.ball_x = self.PADDLE_WIDTH + self.BALL_SIZE
            # Add angle based on where the ball hits the paddle
            relative_intersect = (self.left_paddle_y - self.ball_y) / (self.PADDLE_HEIGHT / 2)
            self.ball_dy -= relative_intersect * 3
        
        # Right paddle collision
        if (self.ball_x + self.BALL_SIZE >= self.CANVAS_WIDTH - self.PADDLE_WIDTH and
            self.right_paddle_y - self.PADDLE_HEIGHT / 2 <= self.ball_y <= self.right_paddle_y + self.PADDLE_HEIGHT / 2):
            self.ball_dx = -self.ball_dx
            self.ball_x = self.CANVAS_WIDTH - self.PADDLE_WIDTH - self.BALL_SIZE
            # Add angle based on where the ball hits the paddle
            relative_intersect = (self.right_paddle_y - self.ball_y) / (self.PADDLE_HEIGHT / 2)
            self.ball_dy -= relative_intersect * 3
        
        # Left side out - right player scores
        if self.ball_x < 0:
            self.right_score += 1
            self.reset_ball()
        
        # Right side out - left player scores
        if self.ball_x > self.CANVAS_WIDTH:
            self.left_score += 1
            self.reset_ball()
        
        # Check win condition
        if self.left_score >= 11 or self.right_score >= 11:
            self.game_over = True
    
    def reset_ball(self):
        """Reset ball to center."""
        self.ball_x = self.CANVAS_WIDTH / 2
        self.ball_y = self.CANVAS_HEIGHT / 2
        self.ball_dx = random.choice([-5, 5])
        self.ball_dy = random.choice([-5, 5])
    
    def draw_game(self):
        """Draw the game on canvas."""
        self.canvas.delete("all")
        
        # Draw center line
        for i in range(0, self.CANVAS_HEIGHT, 10):
            self.canvas.create_line(
                self.CANVAS_WIDTH / 2, i,
                self.CANVAS_WIDTH / 2, i + 5,
                fill='#7f8c8d',
                width=2
            )
        
        # Draw left paddle
        left_x1 = 10
        left_y1 = self.left_paddle_y - self.PADDLE_HEIGHT / 2
        left_x2 = 10 + self.PADDLE_WIDTH
        left_y2 = self.left_paddle_y + self.PADDLE_HEIGHT / 2
        self.canvas.create_rectangle(left_x1, left_y1, left_x2, left_y2, fill='#3498db', outline='#3498db')
        
        # Draw right paddle
        right_x1 = self.CANVAS_WIDTH - 10 - self.PADDLE_WIDTH
        right_y1 = self.right_paddle_y - self.PADDLE_HEIGHT / 2
        right_x2 = self.CANVAS_WIDTH - 10
        right_y2 = self.right_paddle_y + self.PADDLE_HEIGHT / 2
        self.canvas.create_rectangle(right_x1, right_y1, right_x2, right_y2, fill='#e74c3c', outline='#e74c3c')
        
        # Draw ball
        ball_x1 = self.ball_x - self.BALL_SIZE
        ball_y1 = self.ball_y - self.BALL_SIZE
        ball_x2 = self.ball_x + self.BALL_SIZE
        ball_y2 = self.ball_y + self.BALL_SIZE
        self.canvas.create_oval(ball_x1, ball_y1, ball_x2, ball_y2, fill='#1a252f', outline='#1a252f')
        
        # Update score label
        self.score_label.config(text=f"Player 1: {self.left_score}  |  Player 2: {self.right_score}")
    
    def game_loop(self):
        """Main game loop."""
        if not self.game_over:
            self.update_paddles()
            self.update_ball()
            self.draw_game()
            self.root.after(self.GAME_SPEED, self.game_loop)
        else:
            winner = "Player 1 (Blue)" if self.left_score >= 11 else "Player 2 (Red)"
            self.canvas.create_text(
                self.CANVAS_WIDTH / 2, self.CANVAS_HEIGHT / 2,
                text=f"{winner} Wins!",
                fill='#f39c12',
                font=('Helvetica', 32, 'bold')
            )
    
    def reset_game(self):
        """Reset the game to initial state."""
        self.left_paddle_y = self.CANVAS_HEIGHT / 2
        self.right_paddle_y = self.CANVAS_HEIGHT / 2
        self.ball_x = self.CANVAS_WIDTH / 2
        self.ball_y = self.CANVAS_HEIGHT / 2
        self.ball_dx = 5
        self.ball_dy = 5
        self.left_score = 0
        self.right_score = 0
        self.game_over = False
        self.draw_game()
        # self.game_loop()


if __name__ == "__main__":
    root = tk.Tk()
    game = PongGame(root)
    root.mainloop()