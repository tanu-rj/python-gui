"""
Flappy Bird Game - GUI Version using Pygame
"""

import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Game constants
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 800
GRAVITY = 0.6
FLAP_POWER = -12
PIPE_GAP = 150
PIPE_SPEED = -4
PIPE_SPAWN_INTERVAL = 2000  # milliseconds

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
GREEN = (34, 139, 34)

class Bird:
    def __init__(self):
        self.x = 100
        self.y = WINDOW_HEIGHT // 2
        self.radius = 15
        self.velocity = 0
    
    def flap(self):
        self.velocity = FLAP_POWER
    
    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
    
    def draw(self, screen):
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.radius)
    
    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, 
                          self.radius * 2, self.radius * 2)

class Pipe:
    def __init__(self, x):
        self.x = x
        self.width = 80
        self.gap_y = random.randint(100, WINDOW_HEIGHT - PIPE_GAP - 100)
        self.gap_size = PIPE_GAP
        self.scored = False
    
    def update(self):
        self.x += PIPE_SPEED
    
    def draw(self, screen):
        # Top pipe
        pygame.draw.rect(screen, GREEN, (self.x, 0, self.width, self.gap_y))
        # Bottom pipe
        pygame.draw.rect(screen, GREEN, (self.x, self.gap_y + self.gap_size, 
                                        self.width, WINDOW_HEIGHT))
    
    def is_off_screen(self):
        return self.x + self.width < 0
    
    def collides(self, bird_rect):
        pipe_rect_top = pygame.Rect(self.x, 0, self.width, self.gap_y)
        pipe_rect_bottom = pygame.Rect(self.x, self.gap_y + self.gap_size, 
                                       self.width, WINDOW_HEIGHT)
        
        return bird_rect.colliderect(pipe_rect_top) or bird_rect.colliderect(pipe_rect_bottom)

class FlappyBirdGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("🐦 Flappy Bird")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 32)
        
        self.reset_game()
    
    def reset_game(self):
        self.bird = Bird()
        self.pipes = []
        self.score = 0
        self.game_over = False
        self.last_pipe_time = 0
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.game_over:
                        self.reset_game()
                    else:
                        self.bird.flap()
                
                if event.key == pygame.K_ESCAPE:
                    return False
        
        return True
    
    def update(self):
        if self.game_over:
            return
        
        self.bird.update()
        
        # Check boundary collision
        if self.bird.y - self.bird.radius < 0 or \
           self.bird.y + self.bird.radius > WINDOW_HEIGHT:
            self.game_over = True
            return
        
        # Spawn new pipes
        current_time = pygame.time.get_ticks()
        if current_time - self.last_pipe_time > PIPE_SPAWN_INTERVAL:
            self.pipes.append(Pipe(WINDOW_WIDTH))
            self.last_pipe_time = current_time
        
        # Update pipes
        for pipe in self.pipes:
            pipe.update()
            
            # Check collision
            if pipe.collides(self.bird.get_rect()):
                self.game_over = True
            
            # Check if bird passed the pipe
            if not pipe.scored and pipe.x + pipe.width < self.bird.x:
                pipe.scored = True
                self.score += 1
        
        # Remove off-screen pipes
        self.pipes = [pipe for pipe in self.pipes if not pipe.is_off_screen()]
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw pipes
        for pipe in self.pipes:
            pipe.draw(self.screen)
        
        # Draw bird
        self.bird.draw(self.screen)
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (20, 20))
        
        if self.game_over:
            game_over_text = self.font.render("GAME OVER!", True, RED)
            restart_text = self.small_font.render("Press SPACE to restart or ESC to exit", True, WHITE)
            
            self.screen.blit(game_over_text, (WINDOW_WIDTH // 2 - 180, WINDOW_HEIGHT // 2 - 50))
            self.screen.blit(restart_text, (WINDOW_WIDTH // 2 - 220, WINDOW_HEIGHT // 2 + 20))
        else:
            instruction_text = self.small_font.render("Press SPACE to flap", True, CYAN)
            self.screen.blit(instruction_text, (WINDOW_WIDTH // 2 - 180, WINDOW_HEIGHT - 50))
        
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)  # 60 FPS
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = FlappyBirdGame()
    game.run()
