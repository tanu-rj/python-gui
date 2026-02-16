"""
Pong Game - GUI Version using Pygame
Two-player classic arcade game
"""

import pygame
import random
import sys

pygame.init()

# Game constants
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)

class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 15, 100)
        self.speed = 7
        self.score = 0
    
    def move_up(self):
        if self.rect.top > 0:
            self.rect.y -= self.speed
    
    def move_down(self):
        if self.rect.bottom < WINDOW_HEIGHT:
            self.rect.y += self.speed
    
    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)

class Ball:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.rect = pygame.Rect(WINDOW_WIDTH // 2 - 5, WINDOW_HEIGHT // 2 - 5, 10, 10)
        self.vx = random.choice([-6, 6])
        self.vy = random.randint(-6, 6)
        self.speed = 6
    
    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        
        # Wall collision (top/bottom)
        if self.rect.top <= 0 or self.rect.bottom >= WINDOW_HEIGHT:
            self.vy = -self.vy
            self.rect.y = max(0, min(WINDOW_HEIGHT - 10, self.rect.y))
    
    def draw(self, screen):
        pygame.draw.ellipse(screen, YELLOW, self.rect)

class PongGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("🏓 Pong")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        
        self.reset_game()
    
    def reset_game(self):
        self.player1 = Paddle(20, WINDOW_HEIGHT // 2 - 50)
        self.player2 = Paddle(WINDOW_WIDTH - 35, WINDOW_HEIGHT // 2 - 50)
        self.ball = Ball()
        self.game_over = False
        self.winner = None
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                
                if event.key == pygame.K_r and self.game_over:
                    self.reset_game()
        
        return True
    
    def update(self):
        if self.game_over:
            return
        
        # Input handling
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player1.move_up()
        if keys[pygame.K_s]:
            self.player1.move_down()
        
        if keys[pygame.K_UP]:
            self.player2.move_up()
        if keys[pygame.K_DOWN]:
            self.player2.move_down()
        
        self.ball.update()
        
        # Paddle collision
        if self.ball.rect.colliderect(self.player1.rect) and self.ball.vx < 0:
            self.ball.vx = -self.ball.vx
            self.ball.rect.x = self.player1.rect.right
            self.ball.vy += random.randint(-3, 3)
            self.player1.score += 1
        
        if self.ball.rect.colliderect(self.player2.rect) and self.ball.vx > 0:
            self.ball.vx = -self.ball.vx
            self.ball.rect.x = self.player2.rect.left - 10
            self.ball.vy += random.randint(-3, 3)
            self.player2.score += 1
        
        # Out of bounds
        if self.ball.rect.left < 0:
            self.player2.score += 10
            self.ball.reset()
        
        if self.ball.rect.right > WINDOW_WIDTH:
            self.player1.score += 10
            self.ball.reset()
        
        # Check win condition
        if self.player1.score >= 100:
            self.game_over = True
            self.winner = "Player 1 (W/S Keys)"
        elif self.player2.score >= 100:
            self.game_over = True
            self.winner = "Player 2 (↑/↓ Keys)"
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw center line
        for y in range(0, WINDOW_HEIGHT, 20):
            pygame.draw.line(self.screen, WHITE, (WINDOW_WIDTH // 2, y), 
                           (WINDOW_WIDTH // 2, y + 10), 2)
        
        # Draw paddles and ball
        self.player1.draw(self.screen)
        self.player2.draw(self.screen)
        self.ball.draw(self.screen)
        
        # Draw scores
        score1_text = self.font_large.render(str(self.player1.score), True, CYAN)
        score2_text = self.font_large.render(str(self.player2.score), True, YELLOW)
        
        self.screen.blit(score1_text, (WINDOW_WIDTH // 4 - 30, 50))
        self.screen.blit(score2_text, (3 * WINDOW_WIDTH // 4 - 30, 50))
        
        # Draw instructions
        instr1 = self.font_small.render("Player 1: W/S", True, CYAN)
        instr2 = self.font_small.render("Player 2: UP/DOWN", True, YELLOW)
        self.screen.blit(instr1, (20, WINDOW_HEIGHT - 60))
        self.screen.blit(instr2, (WINDOW_WIDTH - 250, WINDOW_HEIGHT - 60))
        
        if self.game_over:
            winner_text = self.font_medium.render(f"{self.winner} Wins!", True, WHITE)
            restart_text = self.font_small.render("Press R to restart", True, WHITE)
            self.screen.blit(winner_text, (WINDOW_WIDTH // 2 - 200, WINDOW_HEIGHT // 2 - 50))
            self.screen.blit(restart_text, (WINDOW_WIDTH // 2 - 140, WINDOW_HEIGHT // 2 + 50))
        
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
    game = PongGame()
    game.run()
