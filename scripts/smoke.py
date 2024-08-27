import math
import random
import pygame

class Smoke:
    def __init__(self, pos, angle, speed):
        self.pos = list(pos)
        self.angle = angle
        self.speed = speed

    def update(self):
        self.pos[0] += math.cos(self.angle) * self.speed
        self.pos[1] += math.sin(self.angle) * self.speed

        self.speed = max(0, self.speed -0.1)
        return not self.speed
    
    def render(self, surf, offset=(0, 0)):
        
        
        rect = pygame.Rect(self.pos[0] - offset[0], self.pos[1] - offset[1], random.randint(2,5), random.randint(3,8))

        pygame.draw.ellipse(surf, (105, 105, 105), rect, 1)