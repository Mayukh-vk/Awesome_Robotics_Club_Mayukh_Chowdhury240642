import pygame
import random
import sys
import time

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
LANE_WIDTH = SCREEN_WIDTH // 2
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Game variables
score = 0
speed = 5
game_over = False
clock = pygame.time.Clock()

class Cat:
    def __init__(self):
        self.width = 40
        self.height = 40
        self.x = LANE_WIDTH // 2  # Start in left lane
        self.y = SCREEN_HEIGHT - 100
        self.lane = 0  # 0 = left, 1 = right

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, (self.x, self.y, self.width, self.height))

    def move(self, direction):
        if direction == "left" and self.lane == 1:
            self.lane = 0
            self.x = LANE_WIDTH // 2
        elif direction == "right" and self.lane == 0:
            self.lane = 1
            self.x = LANE_WIDTH + (LANE_WIDTH // 2)

class Obstacle:
    def __init__(self):
        self.width = 50
        self.height = 50
        self.lane = random.randint(0, 1)
        self.x = (LANE_WIDTH // 2) if self.lane == 0 else (LANE_WIDTH + (LANE_WIDTH // 2))
        self.y = -self.height

    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))

    def update(self):
        self.y += speed

class PowerUp:
    def __init__(self):
        self.width = 30
        self.height = 30
        self.type = random.choice(["speed", "shield", "score"])
        self.lane = random.randint(0, 1)
        self.x = (LANE_WIDTH // 2) if self.lane == 0 else (LANE_WIDTH + (LANE_WIDTH // 2))
        self.y = -self.height
        self.color = {
            "speed": (0, 255, 255),    # Cyan
            "shield": (255, 215, 0),    # Gold
            "score": (255, 192, 203)    # Pink
        }[self.type]

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def update(self):
        self.y += speed

def main():
    global score, speed, game_over

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Cat Runner")

    cat = Cat()
    obstacles = []
    power_ups = []
    obstacle_spawn_timer = 0
    power_up_timer = 0
    active_power_up = None
    power_up_end_time = 0

    # Main game loop
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    cat.move("left")
                elif event.key == pygame.K_d:
                    cat.move("right")

        # Spawn obstacles
        obstacle_spawn_timer += 1
        if obstacle_spawn_timer > 60:
            obstacles.append(Obstacle())
            obstacle_spawn_timer = 0

        # Spawn power-ups
        power_up_timer += 1
        if power_up_timer > 180:
            power_ups.append(PowerUp())
            power_up_timer = 0

        # Update obstacles
        for obstacle in obstacles[:]:
            obstacle.update()
            if obstacle.y > SCREEN_HEIGHT:
                obstacles.remove(obstacle)
                score += 2 if active_power_up == "score" else 1

            # Collision detection (skip if shield is active)
            if active_power_up != "shield":
                if (cat.x < obstacle.x + obstacle.width and
                    cat.x + cat.width > obstacle.x and
                    cat.y < obstacle.y + obstacle.height and
                    cat.y + cat.height > obstacle.y):
                    game_over = True

        # Update power-ups
        for power_up in power_ups[:]:
            power_up.update()
            if power_up.y > SCREEN_HEIGHT:
                power_ups.remove(power_up)

            # Power-up collision
            if (cat.x < power_up.x + power_up.width and
                cat.x + cat.width > power_up.x and
                cat.y < power_up.y + power_up.height and
                cat.y + cat.height > power_up.y):
                active_power_up = power_up.type
                power_up_end_time = pygame.time.get_ticks() + {
                    "speed": 3000,
                    "shield": 3000,
                    "score": 5000
                }[active_power_up]
                power_ups.remove(power_up)

        # Check power-up expiration
        current_time = pygame.time.get_ticks()
        if active_power_up and current_time > power_up_end_time:
            active_power_up = None

        # Adjust speed if speed boost is active
        current_speed = speed * 1.5 if active_power_up == "speed" else speed

        # Increase difficulty
        if score % 10 == 0:
            speed += 0.1

        # Draw everything
        screen.fill(BLACK)
        cat.draw(screen)
        for obstacle in obstacles:
            obstacle.draw(screen)
        for power_up in power_ups:
            power_up.draw(screen)

        # Display score and power-up status
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        if active_power_up:
            status_text = font.render(f"Power: {active_power_up}", True, WHITE)
            screen.blit(status_text, (10, 50))

        pygame.display.flip()
        clock.tick(60)

    # Game over screen
    font = pygame.font.SysFont(None, 72)
    game_over_text = font.render("GAME OVER", True, WHITE)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 36))
    pygame.display.flip()
    pygame.time.wait(2000)

if __name__ == "__main__":
    main()
