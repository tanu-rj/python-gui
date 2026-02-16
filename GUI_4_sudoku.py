"""
Sudoku Game - GUI Version using Pygame
"""

import pygame
import sys

# Initialize Pygame
pygame.init()

# Game constants
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 900
GRID_SIZE = 9
CELL_SIZE = WINDOW_WIDTH // GRID_SIZE
BOX_SIZE = 3

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (220, 220, 220)
DARK_GRAY = (100, 100, 100)
BLUE = (100, 150, 255)
RED = (255, 100, 100)
GREEN = (100, 255, 100)
YELLOW = (255, 255, 100)
NAVY = (0, 0, 139)

# Sample Sudoku puzzles (0 = empty)
PUZZLES = [
    [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ],
    [
        [0, 0, 0, 2, 6, 0, 7, 0, 1],
        [6, 0, 0, 0, 7, 0, 0, 0, 0],
        [0, 9, 0, 0, 0, 4, 5, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 9],
        [9, 0, 0, 0, 0, 0, 0, 0, 5],
        [0, 0, 5, 0, 0, 2, 0, 0, 0],
        [0, 0, 9, 3, 0, 0, 0, 2, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 3],
        [8, 0, 3, 0, 2, 5, 0, 0, 0]
    ]
]

class SudokuGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("🔢 Sudoku")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        self.init_game()
    
    def init_game(self):
        import copy
        puzzle = PUZZLES[0]  # Use first puzzle
        
        self.board = copy.deepcopy(puzzle)
        self.solution = copy.deepcopy(puzzle)
        self.solve_sudoku(self.solution)
        
        self.player_board = copy.deepcopy(puzzle)
        self.selected_cell = None
        self.selected_number = None
        self.mistakes = 0
        self.max_mistakes = 3
        self.game_over = False
        self.won = False
    
    def solve_sudoku(self, board):
        """Simple backtracking solver"""
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if board[row][col] == 0:
                    for num in range(1, 10):
                        if self.is_valid(board, row, col, num):
                            board[row][col] = num
                            if self.solve_sudoku(board):
                                return True
                            board[row][col] = 0
                    return False
        return True
    
    def is_valid(self, board, row, col, num):
        # Check row
        if num in board[row]:
            return False
        
        # Check column
        if num in [board[i][col] for i in range(GRID_SIZE)]:
            return False
        
        # Check 3x3 box
        box_row, box_col = (row // BOX_SIZE) * BOX_SIZE, (col // BOX_SIZE) * BOX_SIZE
        for i in range(box_row, box_row + BOX_SIZE):
            for j in range(box_col, box_col + BOX_SIZE):
                if board[i][j] == num:
                    return False
        
        return True
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                
                if event.key == pygame.K_r and (self.game_over or self.won):
                    self.init_game()
                
                if self.selected_cell and not self.game_over and not self.won:
                    row, col = self.selected_cell
                    
                    # Only allow input on empty cells
                    if self.board[row][col] == 0:
                        if pygame.K_1 <= event.key <= pygame.K_9:
                            num = event.key - pygame.K_0
                            if self.is_valid(self.player_board, row, col, num):
                                self.player_board[row][col] = num
                            else:
                                self.mistakes += 1
                                if self.mistakes >= self.max_mistakes:
                                    self.game_over = True
                        
                        elif event.key == pygame.K_0 or event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                            self.player_board[row][col] = 0
                    
                    # Check if won
                    if self.is_complete(self.player_board):
                        self.won = True
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                col = x // CELL_SIZE
                row = y // CELL_SIZE
                if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                    self.selected_cell = (row, col)
        
        return True
    
    def is_complete(self, board):
        for row in board:
            if 0 in row:
                return False
        return True
    
    def draw(self):
        self.screen.fill(WHITE)
        
        # Draw grid
        for i in range(GRID_SIZE + 1):
            thickness = 3 if i % BOX_SIZE == 0 else 1
            pygame.draw.line(self.screen, BLACK, (i * CELL_SIZE, 0), 
                           (i * CELL_SIZE, WINDOW_HEIGHT), thickness)
            pygame.draw.line(self.screen, BLACK, (0, i * CELL_SIZE), 
                           (WINDOW_WIDTH, i * CELL_SIZE), thickness)
        
        # Draw numbers
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                x = col * CELL_SIZE + CELL_SIZE // 2
                y = row * CELL_SIZE + CELL_SIZE // 2
                
                # Highlight selected cell
                if self.selected_cell == (row, col):
                    pygame.draw.rect(self.screen, YELLOW, 
                                   (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                
                # Draw given numbers (darker)
                if self.board[row][col] != 0:
                    num_text = self.font_large.render(str(self.board[row][col]), True, BLACK)
                    self.screen.blit(num_text, (x - 20, y - 25))
                # Draw player numbers
                elif self.player_board[row][col] != 0:
                    num_text = self.font_large.render(str(self.player_board[row][col]), True, BLUE)
                    self.screen.blit(num_text, (x - 20, y - 25))
        
        # Draw status bar
        pygame.draw.rect(self.screen, LIGHT_GRAY, (0, WINDOW_HEIGHT - 60, WINDOW_WIDTH, 60))
        
        status_text = f"Mistakes: {self.mistakes}/{self.max_mistakes}"
        status = self.font_small.render(status_text, True, RED if self.mistakes >= 2 else BLACK)
        self.screen.blit(status, (20, WINDOW_HEIGHT - 50))
        
        if self.game_over:
            game_over_text = self.font_large.render("GAME OVER!", True, RED)
            restart_text = self.font_small.render("Press R to restart", True, BLACK)
            self.screen.blit(game_over_text, (WINDOW_WIDTH // 2 - 180, WINDOW_HEIGHT // 2 - 50))
            self.screen.blit(restart_text, (WINDOW_WIDTH // 2 - 120, WINDOW_HEIGHT // 2 + 30))
        
        elif self.won:
            won_text = self.font_large.render("YOU WON!", True, GREEN)
            restart_text = self.font_small.render("Press R to play again", True, BLACK)
            self.screen.blit(won_text, (WINDOW_WIDTH // 2 - 140, WINDOW_HEIGHT // 2 - 50))
            self.screen.blit(restart_text, (WINDOW_WIDTH // 2 - 140, WINDOW_HEIGHT // 2 + 30))
        
        pygame.display.flip()
    
    def run(self):
        running = True
        
        while running:
            running = self.handle_events()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = SudokuGame()
    game.run()
