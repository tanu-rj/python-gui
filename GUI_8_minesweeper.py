"""
Minesweeper Game - GUI Version using Pygame
"""

import pygame
import random
import sys

pygame.init()

# Game constants
BOARD_SIZE = 10
MINES = 10
CELL_SIZE = 40
WINDOW_SIZE = BOARD_SIZE * CELL_SIZE
MARGIN = 50
WINDOW_WIDTH = WINDOW_SIZE + 2 * MARGIN
WINDOW_HEIGHT = WINDOW_SIZE + 2 * MARGIN + 50
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
LIGHT_GRAY = (220, 220, 220)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.mine_count = 0
        self.rect = pygame.Rect(MARGIN + x * CELL_SIZE, MARGIN + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    
    def draw(self, screen, font_small):
        if not self.is_revealed:
            # Unrevealed cell
            color = LIGHT_GRAY if not self.is_flagged else YELLOW
            pygame.draw.rect(screen, color, self.rect)
            pygame.draw.rect(screen, DARK_GRAY, self.rect, 2)
            
            if self.is_flagged:
                flag_text = font_small.render("🚩", True, RED)
                screen.blit(flag_text, (self.rect.x + 10, self.rect.y + 5))
        else:
            # Revealed cell
            pygame.draw.rect(screen, GRAY, self.rect)
            pygame.draw.rect(screen, DARK_GRAY, self.rect, 1)
            
            if self.is_mine:
                pygame.draw.circle(screen, RED, self.rect.center, CELL_SIZE // 4)
            elif self.mine_count > 0:
                color_map = {1: BLUE, 2: GREEN, 3: RED, 4: DARK_GRAY, 
                            5: RED, 6: BLACK, 7: BLACK, 8: DARK_GRAY}
                color = color_map.get(self.mine_count, BLACK)
                text = font_small.render(str(self.mine_count), True, color)
                screen.blit(text, (self.rect.x + 12, self.rect.y + 8))

class MinesweeperGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("💣 Minesweeper")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        self.reset_game()
    
    def reset_game(self):
        self.board = [[Cell(x, y) for x in range(BOARD_SIZE)] for y in range(BOARD_SIZE)]
        self.place_mines()
        self.game_over = False
        self.won = False
        self.first_click = True
    
    def place_mines(self):
        mines_placed = 0
        while mines_placed < MINES:
            x = random.randint(0, BOARD_SIZE - 1)
            y = random.randint(0, BOARD_SIZE - 1)
            
            if not self.board[y][x].is_mine:
                self.board[y][x].is_mine = True
                mines_placed += 1
        
        # Calculate mine counts
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                if not self.board[y][x].is_mine:
                    count = 0
                    for dy in [-1, 0, 1]:
                        for dx in [-1, 0, 1]:
                            ny, nx = y + dy, x + dx
                            if 0 <= ny < BOARD_SIZE and 0 <= nx < BOARD_SIZE:
                                if self.board[ny][nx].is_mine:
                                    count += 1
                    self.board[y][x].mine_count = count
    
    def reveal_cell(self, x, y):
        if x < 0 or x >= BOARD_SIZE or y < 0 or y >= BOARD_SIZE:
            return
        
        cell = self.board[y][x]
        
        if cell.is_revealed or cell.is_flagged:
            return
        
        cell.is_revealed = True
        
        if cell.is_mine:
            self.game_over = True
            self.reveal_all_mines()
            return
        
        # Flood fill for empty cells
        if cell.mine_count == 0:
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    self.reveal_cell(x + dx, y + dy)
    
    def reveal_all_mines(self):
        for row in self.board:
            for cell in row:
                if cell.is_mine:
                    cell.is_revealed = True
    
    def check_win(self):
        for row in self.board:
            for cell in row:
                if not cell.is_mine and not cell.is_revealed:
                    return False
        return True
    
    def flag_cell(self, x, y):
        if x < 0 or x >= BOARD_SIZE or y < 0 or y >= BOARD_SIZE:
            return
        
        cell = self.board[y][x]
        if not cell.is_revealed:
            cell.is_flagged = not cell.is_flagged
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                
                if event.key == pygame.K_r and (self.game_over or self.won):
                    self.reset_game()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                
                # Check if click is on board
                if MARGIN <= mouse_x < MARGIN + WINDOW_SIZE and \
                   MARGIN <= mouse_y < MARGIN + WINDOW_SIZE:
                    x = (mouse_x - MARGIN) // CELL_SIZE
                    y = (mouse_y - MARGIN) // CELL_SIZE
                    
                    if event.button == 1:  # Left click
                        if self.first_click:
                            self.first_click = False
                        self.reveal_cell(x, y)
                        if self.check_win():
                            self.won = True
                    
                    elif event.button == 3:  # Right click
                        self.flag_cell(x, y)
        
        return True
    
    def update(self):
        pass
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw board background
        pygame.draw.rect(self.screen, DARK_GRAY, 
                        (MARGIN, MARGIN, WINDOW_SIZE, WINDOW_SIZE))
        
        # Draw cells
        for row in self.board:
            for cell in row:
                cell.draw(self.screen, self.font_small)
        
        # Draw status bar
        status_text = f"Left Click: Reveal | Right Click: Flag"
        status = self.font_small.render(status_text, True, WHITE)
        self.screen.blit(status, (20, 10))
        
        if self.game_over:
            game_over_text = self.font_large.render("GAME OVER!", True, RED)
            restart_text = self.font_medium.render("Press R to restart", True, WHITE)
            self.screen.blit(game_over_text, (WINDOW_WIDTH // 2 - 180, WINDOW_HEIGHT - 80))
            self.screen.blit(restart_text, (WINDOW_WIDTH // 2 - 160, WINDOW_HEIGHT - 30))
        
        elif self.won:
            won_text = self.font_large.render("YOU WON!", True, GREEN)
            restart_text = self.font_medium.render("Press R to restart", True, WHITE)
            self.screen.blit(won_text, (WINDOW_WIDTH // 2 - 140, WINDOW_HEIGHT - 80))
            self.screen.blit(restart_text, (WINDOW_WIDTH // 2 - 160, WINDOW_HEIGHT - 30))
        
        pygame.display.flip()
    
    def run(self):
        running = True
        
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = MinesweeperGame()
    game.run()
