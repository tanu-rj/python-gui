"""
Fruit Slash Game - GUI Version using Pygame
Slash fruits to gain points
"""

import pygame
import random
import sys
import math

# Initialize Pygame
pygame.init()

# Game constants
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
FPS = 60

# Colors
BLACK = (20, 20, 40)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
PURPLE = (200, 0, 255)

class Fruit:
    def __init__(self, x, y, fruit_type):
        self.x = x
        self.y = y
        self.fruit_type = fruit_type  # 'apple', 'orange', 'bomb'
        self.vx = random.uniform(-8, 8)
        self.vy = random.uniform(-15, -5)
        self.radius = 20
        self.slashed = False
        self.age = 0
        
        # Fruit colors
        self.colors = {
            'apple': RED,
            'orange': ORANGE,
            'bomb': PURPLE,
            'special': YELLOW
        }
    
    def update(self):
        self.vy += 0.5  # Gravity
        self.x += self.vx
        self.y += self.vy
        self.age += 1
    
    def draw(self, screen):
        if self.slashed:
            # Draw slash effect
            pygame.draw.circle(screen, CYAN, (int(self.x), int(self.y)), self.radius + 5, 2)
        else:
            color = self.colors.get(self.fruit_type, RED)
            pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius)
            # Draw shine
            pygame.draw.circle(screen, WHITE, (int(self.x - 7), int(self.y - 7)), 4)
    
    def is_off_screen(self):
        return self.y > WINDOW_HEIGHT + 50
    
    def is_slashed(self, mouse_x, mouse_y):
        dist = math.sqrt((self.x - mouse_x) ** 2 + (self.y - mouse_y) ** 2)
        return dist < self.radius + 10

class FruitSlashGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("🍎 Fruit Slash")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 32)
        
        self.reset_game()
    
    def reset_game(self):
        self.fruits = []
        self.score = 0
        self.combo = 0
        self.lives = 3
        self.game_over = False
        self.time_survived = 0
        self.spawn_counter = 0
        self.max_fruits = 5
    
    def spawn_fruit(self):
        x = random.randint(50, WINDOW_WIDTH - 50)
        y = WINDOW_HEIGHT + 30
        
        rand = random.random()
        if rand < 0.1:
            fruit_type = 'bomb'
        elif rand < 0.25:
            fruit_type = 'special'
        elif rand < 0.6:
            fruit_type = 'apple'
        else:
            fruit_type = 'orange'
        
        self.fruits.append(Fruit(x, y, fruit_type))
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                
                if event.key == pygame.K_SPACE and self.game_over:
                    self.reset_game()
        
        return True
    
    def update(self):
        if self.game_over:
            return
        
        self.time_survived += 1
        self.spawn_counter += 1
        
        # Increase spawn rate with time
        spawn_rate = 40 - min(self.time_survived // 1000, 25)
        
        if self.spawn_counter > spawn_rate and len(self.fruits) < self.max_fruits + (self.time_survived // 3000):
            self.spawn_fruit()
            self.spawn_counter = 0
        
        # Update fruits
        for fruit in self.fruits:
            fruit.update()
        
        # Remove off-screen fruits
        for fruit in self.fruits:
            if fruit.is_off_screen() and not fruit.slashed:
                self.fruits.remove(fruit)
                self.lives -= 1
                self.combo = 0
                if self.lives <= 0:
                    self.game_over = True
        
        # Remove slashed fruits after delay
        self.fruits = [fruit for fruit in self.fruits if not (fruit.slashed and fruit.age > 10)]
    
    def handle_slash(self, mouse_x, mouse_y):
        for fruit in self.fruits:
            if not fruit.slashed and fruit.is_slashed(mouse_x, mouse_y):
                fruit.slashed = True
                
                if fruit.fruit_type == 'bomb':
                    self.lives -= 1
                    self.combo = 0
                    if self.lives <= 0:
                        self.game_over = True
                else:
                    self.combo += 1
                    points = 10 if fruit.fruit_type in ['apple', 'orange'] else 25
                    if fruit.fruit_type == 'special':
                        points = 50
                    
                    self.score += points * self.combo
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw fruits
        for fruit in self.fruits:
            fruit.draw(self.screen)
        
        # Draw UI
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        combo_text = self.small_font.render(f"Combo: {self.combo}x", True, YELLOW if self.combo > 0 else WHITE)
        lives_text = self.small_font.render(f"Lives: {self.lives}", True, RED if self.lives <= 1 else WHITE)
        
        self.screen.blit(score_text, (20, 20))
        self.screen.blit(combo_text, (WINDOW_WIDTH - 200, 20))
        self.screen.blit(lives_text, (WINDOW_WIDTH // 2 - 50, 20))
        
        # Draw instructions
        instr_text = self.small_font.render("Click and drag to slash fruits!", True, CYAN)
        self.screen.blit(instr_text, (WINDOW_WIDTH // 2 - 200, WINDOW_HEIGHT - 40))
        
        if self.game_over:
            game_over_text = self.font.render("GAME OVER!", True, RED)
            final_score_text = self.small_font.render(f"Final Score: {self.score}", True, WHITE)
            restart_text = self.small_font.render("Press SPACE to restart", True, WHITE)
            
            self.screen.blit(game_over_text, (WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2 - 80))
            self.screen.blit(final_score_text, (WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2))
            self.screen.blit(restart_text, (WINDOW_WIDTH // 2 - 170, WINDOW_HEIGHT // 2 + 80))
        
        pygame.display.flip()
    
    def run(self):
        running = True
        slash_active = False
        
        while running:
            running = self.handle_events()
            
            # Handle mouse slash
            if pygame.mouse.get_pressed()[0]:  # Left click
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.handle_slash(mouse_x, mouse_y)
            
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = FruitSlashGame()
    game.run()
