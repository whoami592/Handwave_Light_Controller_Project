import pygame
import math
import random
import asyncio
import platform

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wave & Light Simulation")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

# Wave parameters
WAVE_HEIGHT = 50
WAVE_SPEED = 0.05
WAVE_FREQ = 0.02

# Particle class for light effect
class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(2, 5)
        self.alpha = random.randint(100, 255)
        self.speed_y = random.uniform(-2, -1)

    def update(self):
        self.y += self.speed_y
        self.alpha -= 2
        if self.alpha < 0:
            self.alpha = 0

    def draw(self):
        surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(surface, (YELLOW[0], YELLOW[1], YELLOW[2], self.alpha), (self.size, self.size), self.size)
        screen.blit(surface, (self.x - self.size, self.y - self.size))

# Font for banner
font = pygame.font.SysFont('arial', 24)

# Banner text
banner_text = "Coded by Pakistani Ethical Hacker Mr Sabaz Ali Khan"
banner = font.render(banner_text, True, WHITE)
banner_rect = banner.get_rect(center=(WIDTH // 2, HEIGHT - 30))

# Particle list
particles = []

def setup():
    global clock
    clock = pygame.time.Clock()

def update_loop():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return

    # Clear screen
    screen.fill(BLACK)

    # Draw wave
    points = []
    for x in range(WIDTH):
        y = HEIGHT // 2 + math.sin(x * WAVE_FREQ + pygame.time.get_ticks() * WAVE_SPEED) * WAVE_HEIGHT
        points.append((x, y))
        # Add particles at wave peaks
        if random.random() < 0.05:
            particles.append(Particle(x, y))

    # Draw wave line
    pygame.draw.lines(screen, BLUE, False, points, 2)

    # Update and draw particles
    for particle in particles[:]:
        particle.update()
        particle.draw()
        if particle.alpha <= 0:
            particles.remove(particle)

    # Draw banner
    screen.blit(banner, banner_rect)

    pygame.display.flip()
    clock.tick(60)

async def main():
    setup()
    while True:
        update_loop()
        await asyncio.sleep(1.0 / 60)

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())