import pygame
import random

# --- Einstellungen ---
pygame.init()
screen_width, screen_height = 300, 600
block_size = 30
cols, rows = screen_width // block_size, screen_height // block_size

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tetris")

clock = pygame.time.Clock()
fps = 60

# Farben
colors = [
    (0, 0, 0),       # Leer
    (0, 255, 255),   # I
    (0, 0, 255),     # J
    (255, 165, 0),   # L
    (255, 255, 0),   # O
    (0, 255, 0),     # S
    (128, 0, 128),   # T
    (255, 0, 0)      # Z
]

# --- Tetromino Formen ---
shapes = [
    [[1, 1, 1, 1]],  # I
    [[2, 0, 0],
     [2, 2, 2]],     # J
    [[0, 0, 3],
     [3, 3, 3]],     # L
    [[4, 4],
     [4, 4]],        # O
    [[0, 5, 5],
     [5, 5, 0]],     # S
    [[0, 6, 0],
     [6, 6, 6]],     # T
    [[7, 7, 0],
     [0, 7, 7]]      # Z
]

# Spielfeld (Matrix)
board = [[0 for _ in range(cols)] for _ in range(rows)]

class Tetromino:
    def __init__(self, shape):
        self.shape = shape
        self.color = shapes.index(shape) + 1
        self.x = cols // 2 - len(shape[0]) // 2
        self.y = 0

    def rotate(self):
        # 90 Grad Drehung der Form
        self.shape = [list(row) for row in zip(*self.shape[::-1])]
        if self.collision():
            # Rückgängig machen, wenn Kollision
            self.shape = [list(row) for row in zip(*self.shape)][::-1]

    def collision(self, dx=0, dy=0):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    nx, ny = self.x + x + dx, self.y + y + dy
                    if nx < 0 or nx >= cols or ny >= rows or (ny >= 0 and board[ny][nx]):
                        return True
        return False

    def lock(self):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    board[self.y + y][self.x + x] = self.color

def clear_lines():
    global board, score, level, lines_cleared
    new_board = [row for row in board if any(cell == 0 for cell in row)]
    cleared = rows - len(new_board)
    if cleared > 0:
        for _ in range(cleared):
            new_board.insert(0, [0 for _ in range(cols)])
        board = new_board
        lines_cleared += cleared
        score += cleared * 100
        if lines_cleared // 10 > level:
            level += 1

def draw_board():
    for y in range(rows):
        for x in range(cols):
            color = colors[board[y][x]]
            pygame.draw.rect(screen, color, (x * block_size, y * block_size, block_size, block_size))
            pygame.draw.rect(screen, (40, 40, 40), (x * block_size, y * block_size, block_size, block_size), 1)

def draw_tetromino(tetromino):
    for y, row in enumerate(tetromino.shape):
        for x, cell in enumerate(row):
            if cell:
                color = colors[tetromino.color]
                pygame.draw.rect(screen, color,
                                 ((tetromino.x + x) * block_size, (tetromino.y + y) * block_size, block_size, block_size))
                pygame.draw.rect(screen, (40, 40, 40),
                                 ((tetromino.x + x) * block_size, (tetromino.y + y) * block_size, block_size, block_size), 1)

def draw_text(text, size, color, x, y):
    font = pygame.font.SysFont("Arial", size, True)
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

# Game Variablen
current_tetromino = Tetromino(random.choice(shapes))
next_tetromino = Tetromino(random.choice(shapes))
fall_time = 0
fall_speed = 0.5  # Sekunden pro Schritt (Level beeinflusst)
score = 0
level = 0
lines_cleared = 0

running = True
while running:
    screen.fill((0, 0, 0))
    fall_time += clock.get_time() / 1000  # Zeit seit letztem Frame in Sekunden

    # Automatischer Fall
    if fall_time > fall_speed - (level * 0.03):
        fall_time = 0
        if not current_tetromino.collision(dy=1):
            current_tetromino.y += 1
        else:
            current_tetromino.lock()
            clear_lines()
            current_tetromino = next_tetromino
            next_tetromino = Tetromino(random.choice(shapes))
            if current_tetromino.collision():
                running = False  # Game Over

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if not current_tetromino.collision(dx=-1):
                    current_tetromino.x -= 1
            elif event.key == pygame.K_RIGHT:
                if not current_tetromino.collision(dx=1):
                    current_tetromino.x += 1
            elif event.key == pygame.K_DOWN:
                if not current_tetromino.collision(dy=1):
                    current_tetromino.y += 1
            elif event.key == pygame.K_UP:
                current_tetromino.rotate()
            elif event.key == pygame.K_SPACE:
                # Hard Drop
                while not current_tetromino.collision(dy=1):
                    current_tetromino.y += 1

    draw_board()
    draw_tetromino(current_tetromino)
    draw_text(f"Score: {score}", 24, (255, 255, 255), 10, 10)
    draw_text(f"Level: {level}", 24, (255, 255, 255), 10, 40)
    draw_text(f"Lines: {lines_cleared}", 24, (255, 255, 255), 10, 70)

    pygame.display.update()
    clock.tick(fps)

# Game Over Bildschirm
screen.fill((0, 0, 0))
draw_text("Game Over", 48, (255, 0, 0), screen_width//2 - 100, screen_height//2 - 50)
draw_text(f"Final Score: {score}", 36, (255, 255, 255), screen_width//2 - 110, screen_height//2)
pygame.display.update()
pygame.time.wait(3000)
pygame.quit()
