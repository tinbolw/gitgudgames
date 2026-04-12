# gitgudgames

A collection of classic games built with Python and Tkinter. This is the Video Games repository for the Git Gud with GitHub Event!

---

## 🎮 Available Games

### Pong

**Game Description:**
Pong is a timeless two-player arcade game where players control paddles on opposite sides of the screen to bounce a ball back and forth. The goal is to get the ball past your opponent's paddle to score points!

**Objective:**
Be the first player to reach 11 points. You win by successfully getting the ball to pass your opponent's paddle.

**Controls:**
- **Player 1 (Blue Paddle):** 
  - `W` - Move paddle up
  - `S` - Move paddle down
- **Player 2 (Red Paddle):**
  - `↑ (Up Arrow)` - Move paddle up
  - `↓ (Down Arrow)` - Move paddle down

**How to Play:**
1. Run `pong.py`
2. Players take turns hitting the ball with their paddles
3. The ball's angle changes based on where it hits your paddle
4. First player to score 11 points wins!

---

### Snake

**Game Description:**
Snake is a classic arcade game where you control a snake that grows every time it eats food. Navigate the snake around the grid, eat as much food as possible, and avoid crashing into walls or yourself!

**Objective:**
Eat food to grow your snake and earn points. The longer your snake becomes, the harder it gets to avoid collision. Each piece of food gives you 10 points!

**Controls:**
- `W` - Move up
- `A` - Move left
- `S` - Move down
- `D` - Move right

**How to Play:**
1. Run `snake.py`
2. Use WASD keys to control the snake's direction
3. Move over the red apple to eat it and gain points
4. Your snake will grow longer with each food consumed
5. Avoid hitting the walls or your own tail
6. Click "New Game" to restart after game over

---

### Connect 4

**Game Description:**
Connect 4 is a turn-based strategy game where two players take turns dropping colored pieces into a grid. The first player to get four pieces in a row (horizontally, vertically, or diagonally) wins the game!

**Objective:**
Drop your colored pieces into columns to create a line of four matching pieces before your opponent does. Think strategically to block your opponent while building your own winning combinations.

**Controls:**
- **Click the down arrow buttons** at the top of each column to drop your piece
- Player 1 uses red pieces, Player 2 uses yellow pieces

**How to Play:**
1. Run `connect4.py`
2. Players alternate turns (Player 1 starts)
3. Click a column button to drop your piece - it will fall to the lowest available position
4. Build horizontal, vertical, or diagonal lines of four of your pieces
5. The first player to connect four wins!
6. Click "New Game" to play again

---

## 🚀 Getting Started

### Requirements
- Python 3.x
- tkinter (usually included with Python)
- numpy (required for Connect 4)

### Installation
Install dependencies:
```bash
pip install numpy
```

### Running a Game
Simply execute any game file with Python:
```bash
python pong.py
python snake.py
python connect4.py
```


---

## 📝 Notes

All games feature a pause-resume capability through the "New Game" button, allowing you to take breaks between matches. Have fun and good luck!

