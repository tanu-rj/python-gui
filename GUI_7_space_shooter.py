"""
Space Shooter Game - GUI Version using Pygame
Shoot down incoming enemies
"""

import pygame
import random
import sys
import math

pygame.init()

# Game constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)

class Player:
    def __init__(self):
        self.width = 40
        self.height = 40
        self.x = WINDOW_WIDTH // 2 - self.width // 2
        self.y = WINDOW_HEIGHT - 60
        self.speed = 5
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x = max(0, self.x - self.speed)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x = min(WINDOW_WIDTH - self.width, self.x + self.speed)
        
        self.rect.x = self.x
    
    def draw(self, screen):
        # Draw player as triangle
        points = [(self.x + self.width // 2, self.y),
                 (self.x, self.y + self.height),
                 (self.x + self.width, self.y + self.height)]
        pygame.draw.polygon(screen, CYAN, points)

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 3
        self.height = 10
        self.speed = 10
        self.rect = pygame.Rect(x, y, self.width, self.height)
    
    def update(self):
        self.y -= self.speed
        self.rect.y = self.y
    
    def draw(self, screen):
        pygame.draw.rect(screen, YELLOW, self.rect)
    
    def is_off_screen(self):
        return self.y < 0

class Enemy:
    def __init__(self, x, y, enemy_type=0):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.speed = random.randint(1, 3)
        self.enemy_type = enemy_type
        self.health = 1 if enemy_type == 0 else 2
        self.rect = pygame.Rect(x, y, self.width, self.height)
    
    def update(self):
        self.y += self.speed
        self.rect.y = self.y
    
    def draw(self, screen):
        if self.enemy_type == 0:
            # Regular enemy
            pygame.draw.rect(screen, RED, self.rect)
            pygame.draw.rect(screen, YELLOW, self.rect, 2)
        else:
            # Strong enemy
            pygame.draw.rect(screen, ORANGE, self.rect)
            pygame.draw.rect(screen, YELLOW, self.rect, 2)
            health_text = pygame.font.Font(None, 16).render(str(self.health), True, WHITE)
            screen.blit(health_text, (self.x + 10, self.y + 10))
    
    def is_off_screen(self):
        return self.y > WINDOW_HEIGHT

class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.age = 0
        self.max_age = 10
    
    def update(self):
        self.age += 1
    
    def draw(self, screen):
        radius = int((self.age / self.max_age) * 20)
        color_value = int(255 * (1 - self.age / self.max_age))
        color = (255, color_value, 0)
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), radius)
    
    def is_finished(self):
        return self.age >= self.max_age

class SpaceShooterGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("🚀 Space Shooter")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        
        self.reset_game()
    
    def reset_game(self):
        self.player = Player()
        self.bullets = []
        self.enemies = []
        self.explosions = []
        self.score = 0
        self.waves = 0
        self.enemies_spawned = 0
        self.lives = 3
        self.game_over = False
        self.spawn_counter = 0
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.shoot()
                
                if event.key == pygame.K_ESCAPE:
                    return False
                
                if event.key == pygame.K_r and self.game_over:
                    self.reset_game()
        
        return True
    
    def shoot(self):
        bullet = Bullet(self.player.x + self.player.width // 2 - 1, self.player.y - 10)
        self.bullets.append(bullet)
    
    def spawn_enemy(self):
        x = random.randint(0, WINDOW_WIDTH - 30)
        y = -30
        enemy_type = 0 if random.random() < 0.8 else 1
        self.enemies.append(Enemy(x, y, enemy_type))
        self.enemies_spawned += 1
    
    def update(self):
        if self.game_over:
            return
        
        self.player.update()
        
        # Update bullets
        for bullet in self.bullets:
            bullet.update()
        
        # Update enemies
        for enemy in self.enemies:
            enemy.update()
        
        # Update explosions
        for explosion in self.explosions:
            explosion.update()
        
        # Remove off-screen bullets and enemies
        self.bullets = [b for b in self.bullets if not b.is_off_screen()]
        
        for enemy in self.enemies:
            if enemy.is_off_screen():
                self.enemies.remove(enemy)
                self.lives -= 1
                if self.lives <= 0:
                    self.game_over = True
        
        # Remove finished explosions
        self.explosions = [e for e in self.explosions if not e.is_finished()]
        
        # Spawn enemies
        self.spawn_counter += 1
        spawn_rate = max(30 - self.waves * 2, 15)
        
        if self.spawn_counter > spawn_rate:
            self.spawn_enemy()
            self.spawn_counter = 0
        
        # Increase waves
        if self.enemies_spawned >= 10 + self.waves * 5:
            self.waves += 1
        
        # Bullet-enemy collision
        for bullet in self.bullets:
            for enemy in self.enemies:
                if bullet.rect.colliderect(enemy.rect):
                    self.bullets.remove(bullet)
                    enemy.health -= 1
                    
                    if enemy.health <= 0:
                        self.enemies.remove(enemy)
                        points = 50 if enemy.enemy_type == 0 else 100
                        self.score += points
                        self.explosions.append(Explosion(enemy.x + 15, enemy.y + 15))
                    break
        
        # Player-enemy collision
        for enemy in self.enemies:
            if self.player.rect.colliderect(enemy.rect):
                self.enemies.remove(enemy)
                self.lives -= 1
                self.explosions.append(Explosion(self.player.x + 20, self.player.y + 20))
                if self.lives <= 0:
                    self.game_over = True
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw stars background
        pygame.draw.circle(self.screen, WHITE, (100, 50), 1)
        pygame.draw.circle(self.screen, WHITE, (200, 100), 1)
        pygame.draw.circle(self.screen, WHITE, (300, 80), 1)
        pygame.draw.circle(self.screen, WHITE, (700, 40), 1)
        
        # Draw game objects
        self.player.draw(self.screen)
        
        for bullet in self.bullets:
            bullet.draw(self.screen)
        
        for enemy in self.enemies:
            enemy.draw(self.screen)
        
        for explosion in self.explosions:
            explosion.draw(self.screen)
        
        # Draw UI
        score_text = self.font_small.render(f"Score: {self.score}", True, WHITE)
        lives_text = self.font_small.render(f"Lives: {self.lives}", True, RED if self.lives <= 1 else WHITE)
        wave_text = self.font_small.render(f"Wave: {self.waves}", True, GREEN)
        
        self.screen.blit(score_text, (20, 10))
        self.screen.blit(lives_text, (WINDOW_WIDTH // 2 - 50, 10))
        self.screen.blit(wave_text, (WINDOW_WIDTH - 150, 10))
        
        if self.game_over:
            game_over_text = self.font_large.render("GAME OVER!", True, RED)
            score_final = self.font_small.render(f"Final Score: {self.score}", True, WHITE)
            restart_text = self.font_small.render("Press R to restart", True, WHITE)
            
            self.screen.blit(game_over_text, (WINDOW_WIDTH // 2 - 180, WINDOW_HEIGHT // 2 - 80))
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
    game = SpaceShooterGame()
    game.run()
