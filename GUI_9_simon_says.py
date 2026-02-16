"""
Simon Says Memory Game - GUI Version using Pygame
Follow the increasingly complex color sequences
"""

import pygame
import random
import sys
import time

pygame.init()

# Game constants
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 700
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (100, 100, 100)

COLORS = [RED, GREEN, BLUE, YELLOW]
COLOR_NAMES = ["Red", "Green", "Blue", "Yellow"]

class SimonButton:
    def __init__(self, x, y, color, size=100):
        self.rect = pygame.Rect(x, y, size, size)
        self.color = color
        self.base_color = color
        self.bright_color = tuple(min(c + 100, 255) for c in color)
        self.is_active = False
    
    def draw(self, screen, is_playing=False):
        color = self.bright_color if self.is_active else self.base_color
        pygame.draw.rect(screen, color, self.rect, border_radius=20)
        pygame.draw.rect(screen, WHITE, self.rect, 3, border_radius=20)
    
    def contains_point(self, x, y):
        return self.rect.collidepoint(x, y)
    
    def activate(self):
        self.is_active = True
    
    def deactivate(self):
        self.is_active = False

class SimonSaysGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("🎮 Simon Says")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        
        # Create buttons
        button_size = 100
        gap = 20
        start_x = (WINDOW_WIDTH - (2 * button_size + gap)) // 2
        start_y = 100
        
        self.buttons = [
            SimonButton(start_x, start_y, RED),  # Red
            SimonButton(start_x + button_size + gap, start_y, GREEN),  # Green
            SimonButton(start_x, start_y + button_size + gap, BLUE),  # Blue
            SimonButton(start_x + button_size + gap, start_y + button_size + gap, YELLOW),  # Yellow
        ]
        
        self.reset_game()
    
    def reset_game(self):
        self.sequence = []
        self.player_sequence = []
        self.level = 0
        self.game_over = False
        self.playing_sequence = False
        self.player_turn = False
        self.game_started = False
        self.sequence_timer = 0
        self.button_press_time = 0
        self.pressed_button = -1
    
    def add_color(self):
        self.sequence.append(random.randint(0, 3))
        self.level += 1
        self.playing_sequence = True
    
    def play_sequence(self):
        if self.sequence_timer > 0:
            self.sequence_timer -= 1
            return
        
        if len(self.sequence) == 0:
            self.playing_sequence = False
            self.player_turn = True
            self.player_sequence = []
            return
        
        # Play next button in sequence
        button_index = len(self.buttons) if not self.sequence else 0
        
        # Flash the button
        if not hasattr(self, '_current_seq_index'):
            self._current_seq_index = 0
        
        if self._current_seq_index < len(self.sequence):
            button_idx = self.sequence[self._current_seq_index]
            self.buttons[button_idx].activate()
            
            if self.sequence_timer == 0:
                self.sequence_timer = 30
            else:
                self.sequence_timer -= 1
            
            if self.sequence_timer <= 0:
                self.buttons[button_idx].deactivate()
                self.sequence_timer = 15
                self._current_seq_index += 1
        
        if self._current_seq_index >= len(self.sequence):
            self._current_seq_index = 0
            self.playing_sequence = False
            self.player_turn = True
            self.player_sequence = []
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                
                if event.key == pygame.K_SPACE and not self.game_started:
                    self.game_started = True
                    self.add_color()
                
                if event.key == pygame.K_r and (self.game_over or (self.game_started and not self.player_turn and not self.sequence)):
                    self.reset_game()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.player_turn and not self.game_over:
                    mouse_x, mouse_y = event.pos
                    
                    for i, button in enumerate(self.buttons):
                        if button.contains_point(mouse_x, mouse_y):
                            self.player_sequence.append(i)
                            self.buttons[i].activate()
                            self.button_press_time = 20
                            
                            # Check if correct
                            if self.player_sequence[-1] != self.sequence[-1 - (len(self.player_sequence) - 1)]:
                                self.game_over = True
                            
                            # Check if completed sequence
                            elif len(self.player_sequence) == len(self.sequence):
                                self.player_turn = False
                                self.add_color()
                            
                            break
        
        return True
    
    def update(self):
        # Update button press time
        if self.button_press_time > 0:
            self.button_press_time -= 1
        else:
            for button in self.buttons:
                if button.is_active:
                    button.deactivate()
        
        # Update sequence playback
        if self.playing_sequence:
            self.play_sequence()
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw title
        if not self.game_started:
            title = self.font_large.render("Simon Says", True, WHITE)
            instr = self.font_small.render("Press SPACE to start", True, WHITE)
            self.screen.blit(title, (WINDOW_WIDTH // 2 - 200, 20))
            self.screen.blit(instr, (WINDOW_WIDTH // 2 - 180, 400))
        else:
            level_text = self.font_medium.render(f"Level: {self.level}", True, WHITE)
            self.screen.blit(level_text, (WINDOW_WIDTH // 2 - 100, 20))
        
        # Draw buttons
        for button in self.buttons:
            button.draw(self.screen, self.playing_sequence)
        
        # Draw status
        status_text = ""
        if self.playing_sequence:
            status_text = "Watch the sequence..."
            status_color = YELLOW
        elif self.player_turn:
            status_text = f"Your turn! ({len(self.player_sequence)}/{len(self.sequence)})"
            status_color = GREEN
        
        if status_text:
            status = self.font_small.render(status_text, True, status_color)
            self.screen.blit(status, (WINDOW_WIDTH // 2 - 200, WINDOW_HEIGHT - 100))
        
        # Draw game over
        if self.game_over:
            game_over_text = self.font_large.render("GAME OVER!", True, RED)
            level_final = self.font_small.render(f"You reached level {self.level}", True, WHITE)
            restart_text = self.font_small.render("Press R to restart", True, WHITE)
            
            self.screen.blit(game_over_text, (WINDOW_WIDTH // 2 - 180, WINDOW_HEIGHT // 2 - 80))
            self.screen.blit(level_final, (WINDOW_WIDTH // 2 - 160, WINDOW_HEIGHT // 2))
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
    game = SimonSaysGame()
    game.run()
