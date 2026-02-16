"""
Breakout / Brick Breaker Game - GUI Version using Pygame
"""

import pygame
import random
import sys

pygame.init()

# Game constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 150, 255)
CYAN = (0, 255, 255)
PINK = (255, 100, 200)

class Paddle:
    def __init__(self):
        self.width = 100
        self.height = 15
        self.x = WINDOW_WIDTH // 2 - self.width // 2
        self.y = WINDOW_HEIGHT - 30
        self.speed = 8
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def update(self):
        mouse_x = pygame.mouse.get_pos()[0]
        self.x = mouse_x - self.width // 2
        self.x = max(0, min(WINDOW_WIDTH - self.width, self.x))
        self.rect.x = self.x
    
    def draw(self, screen):
        pygame.draw.rect(screen, CYAN, self.rect, border_radius=5)

class Ball:
    def __init__(self, paddle):
        self.paddle = paddle
        self.radius = 6
        self.reset_to_paddle()
    
    def reset_to_paddle(self):
        self.x = self.paddle.x + self.paddle.width // 2
        self.y = self.paddle.y - self.radius - 5
        self.vx = random.choice([-4, 4])
        self.vy = -6
        self.attached = True
    
    def update(self, paddle):
        if self.attached:
            self.x = paddle.x + paddle.width // 2
            self.y = paddle.y - self.radius - 5
            return
        
        self.x += self.vx
        self.y += self.vy
        
        # Wall collisions
        if self.x - self.radius < 0 or self.x + self.radius > WINDOW_WIDTH:
            self.vx = -self.vx
            self.x = max(self.radius, min(WINDOW_WIDTH - self.radius, self.x))
        
        if self.y - self.radius < 0:
            self.vy = -self.vy
            self.y = self.radius
        
        # Paddle collision
        if self.y + self.radius > paddle.y and \
           self.y - self.radius < paddle.y + paddle.height and \
           self.x > paddle.x and self.x < paddle.x + paddle.width:
            self.vy = -self.vy
            self.y = paddle.y - self.radius - 2
            # Add spin based on hit location
            hit_pos = (self.x - paddle.x) / paddle.width
            self.vx += (hit_pos - 0.5) * 4
    
    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius)
    
    def is_dead(self):
        return self.y > WINDOW_HEIGHT

class Brick:
    def __init__(self, x, y, color, points=10):
        self.rect = pygame.Rect(x, y, 60, 15)
        self.color = color
        self.points = points
        self.alive = True
    
    def draw(self, screen):
        if self.alive:
            pygame.draw.rect(screen, self.color, self.rect, border_radius=3)
            pygame.draw.rect(screen, WHITE, self.rect, 1, border_radius=3)

class BreakoutGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("🧱 Breakout")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        
        self.reset_game()
    
    def reset_game(self):
        self.paddle = Paddle()
        self.ball = Ball(self.paddle)
        self.bricks = []
        self.score = 0
        self.level = 1
        self.lives = 3
        self.game_over = False
        self.won = False
        
        self.create_bricks()
    
    def create_bricks(self):
        self.bricks = []
        colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PINK]
        
        for row in range(6):
            for col in range(10):
                x = col * 70 + 20
                y = row * 20 + 40
                color = colors[row % len(colors)]
                self.bricks.append(Brick(x, y, color, (6 - row) * 10))
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.ball.attached:
                    self.ball.attached = False
                
                if event.key == pygame.K_ESCAPE:
                    return False
                
                if event.key == pygame.K_r and (self.game_over or self.won):
                    self.reset_game()
        
        return True
    
    def update(self):
        if self.game_over or self.won:
            return
        
        self.paddle.update()
        self.ball.update(self.paddle)
        
        # Ball brick collision
        for brick in self.bricks:
            if brick.alive and self.ball.rect.colliderect(brick.rect):
                brick.alive = False
                self.score += brick.points
                self.ball.vy = -self.ball.vy
                break
        
        # Check if ball is dead
        if self.ball.is_dead():
            self.lives -= 1
            if self.lives <= 0:
                self.game_over = True
            else:
                self.ball.reset_to_paddle()
        
        # Check if all bricks are destroyed
        if all(not brick.alive for brick in self.bricks):
            self.won = True
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw bricks
        for brick in self.bricks:
            brick.draw(self.screen)
        
        # Draw paddle and ball
        self.paddle.draw(self.screen)
        self.ball.draw(self.screen)
        
        # Draw UI
        score_text = self.font_small.render(f"Score: {self.score}", True, WHITE)
        lives_text = self.font_small.render(f"Lives: {self.lives}", True, RED if self.lives <= 1 else WHITE)
        level_text = self.font_small.render(f"Level: {self.level}", True, GREEN)
        
        self.screen.blit(score_text, (20, 10))
        self.screen.blit(lives_text, (WINDOW_WIDTH // 2 - 50, 10))
        self.screen.blit(level_text, (WINDOW_WIDTH - 150, 10))
        
        if self.ball.attached:
            instr = self.font_small.render("Press SPACE to launch", True, CYAN)
            self.screen.blit(instr, (WINDOW_WIDTH // 2 - 160, WINDOW_HEIGHT - 25))
        
        if self.game_over:
            game_over_text = self.font_large.render("GAME OVER!", True, RED)
            restart_text = self.font_small.render("Press R to restart", True, WHITE)
            self.screen.blit(game_over_text, (WINDOW_WIDTH // 2 - 180, WINDOW_HEIGHT // 2 - 50))
            self.screen.blit(restart_text, (WINDOW_WIDTH // 2 - 140, WINDOW_HEIGHT // 2 + 30))
        
        elif self.won:
            won_text = self.font_large.render("YOU WIN!", True, GREEN)
            score_final = self.font_small.render(f"Final Score: {self.score}", True, WHITE)
            restart_text = self.font_small.render("Press R to restart", True, WHITE)
            self.screen.blit(won_text, (WINDOW_WIDTH // 2 - 130, WINDOW_HEIGHT // 2 - 80))
            self.screen.blit(score_final, (WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2))
            self.screen.blit(restart_text, (WINDOW_WIDTH // 2 - 140, WINDOW_HEIGHT // 2 + 80))
        
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
    game = BreakoutGame()
    game.run()
