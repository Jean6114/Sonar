import pygame
import math
import random
import numpy as np

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SONAR Compromised Area Detection")
font = pygame.font.SysFont('Arial', 18)

# Colors
DARK_BLUE = (5, 20, 50)
LIGHT_BLUE = (0, 150, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# SONAR parameters
class Sonar:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pulse_radius = 0
        self.max_range = 400
        self.beam_angle = 60  # degrees
        self.pulse_speed = 5
        self.active = False
        self.detections = []
    
    def ping(self):
        self.active = True
        self.pulse_radius = 0
        self.detections = []
    
    def update(self, seabed, mines):
        if not self.active:
            return
        
        self.pulse_radius += self.pulse_speed
        if self.pulse_radius > self.max_range:
            self.active = False
            return
        
        # Check for seabed collisions
        for x in range(WIDTH):
            seabed_y = seabed[x]
            dist = math.sqrt((x - self.x)**2 + (seabed_y - self.y)**2)
            angle = math.degrees(math.atan2(seabed_y - self.y, x - self.x))
            
            if abs(angle) < self.beam_angle/2 and abs(dist - self.pulse_radius) < 5:
                self.detections.append((x, seabed_y, "seabed"))
        
        # Check for mines in compromised area
        for mine in mines:
            dist = math.sqrt((mine[0] - self.x)**2 + (mine[1] - self.y)**2)
            angle = math.degrees(math.atan2(mine[1] - self.y, mine[0] - self.x))
            
            if abs(angle) < self.beam_angle/2 and abs(dist - self.pulse_radius) < 10:
                self.detections.append((mine[0], mine[1], "mine"))

# Generate seabed with random terrain
def generate_seabed():
    x = np.arange(0, WIDTH)
    y = 400 + 30 * np.sin(x/50) + 20 * np.sin(x/20)
    return y.astype(int)

# Generate compromised area (mines)
def generate_mines(seabed):
    mines = []
    for x in range(300, 700, 30):
        y = seabed[x] - random.randint(10, 30)
        mines.append((x, y))
    return mines

# Boat class
class Boat:
    def __init__(self):
        self.x = 100
        self.y = 300
        self.speed = 2
        self.width = 40
        self.height = 15
        self.sonar = Sonar(self.x + self.width, self.y)
    
    def move(self):
        self.x += self.speed
        self.sonar.x = self.x + self.width
        if self.x > WIDTH:
            self.x = -self.width
    
    def draw(self):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, RED, (self.x + self.width - 10, self.y - 10, 10, 10))  # SONAR housing

# Main game loop
def main():
    clock = pygame.time.Clock()
    seabed = generate_seabed()
    mines = generate_mines(seabed)
    boat = Boat()
    auto_ping = 0
    danger_zones = []
    
    running = True
    while running:
        screen.fill(DARK_BLUE)
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    boat.sonar.ping()
        
        # Update
        boat.move()
        boat.sonar.update(seabed, mines)
        
        # Auto-ping every 60 frames
        auto_ping += 1
        if auto_ping >= 60:
            boat.sonar.ping()
            auto_ping = 0
        
        # Remember danger zones
        for det in boat.sonar.detections:
            if det[2] == "mine" and det not in danger_zones:
                danger_zones.append((det[0], det[1]))
        
        # Draw seabed
        for x in range(WIDTH - 1):
            pygame.draw.line(screen, GREEN, (x, seabed[x]), (x+1, seabed[x+1]), 2)
        
        # Draw compromised area (mines)
        for mine in mines:
            pygame.draw.circle(screen, YELLOW, mine, 5)
        
        # Draw danger zones
        for zone in danger_zones:
            pygame.draw.circle(screen, RED, zone, 8, 1)
        
        # Draw SONAR
        if boat.sonar.active:
            # SONAR beam
            angle = math.radians(boat.sonar.beam_angle / 2)
            points = [
                (boat.sonar.x, boat.sonar.y),
                (boat.sonar.x + boat.sonar.pulse_radius * math.cos(-angle), 
                boat.sonar.y + boat.sonar.pulse_radius * math.sin(-angle)),
                (boat.sonar.x + boat.sonar.pulse_radius * math.cos(angle), 
                boat.sonar.y + boat.sonar.pulse_radius * math.sin(angle))
            ]
            pygame.draw.polygon(screen, (*LIGHT_BLUE, 50), points)
            
            # Detections
            for det in boat.sonar.detections:
                color = RED if det[2] == "mine" else GREEN
                pygame.draw.circle(screen, color, (det[0], det[1]), 5)
                # Echo lines
                pygame.draw.line(screen, (*color, 100), (boat.sonar.x, boat.sonar.y), (det[0], det[1]), 1)
        
        # Draw boat
        boat.draw()
        
        # UI
        info_text = [
            "SONAR Simulation: Compromised Area Detection",
            "[SPACE] Manual Ping | Auto-ping every 2 seconds",
            f"Boat Position: {boat.x:.0f}, {boat.y:.0f}",
            "Green: Seabed | Yellow: Mines | Red: Detected Danger"
        ]
        
        for i, text in enumerate(info_text):
            text_surface = font.render(text, True, WHITE)
            screen.blit(text_surface, (10, 10 + i * 20))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()