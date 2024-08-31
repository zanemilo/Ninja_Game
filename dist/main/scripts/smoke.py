import math
import random
import pygame

class Smoke:
    def __init__(self, pos, angle, speed):
        self.pos = list(pos)
        self.angle = angle
        self.speed = speed
        self.size = random.randint(3, 5)

    def update(self):
        self.pos[0] += math.cos(self.angle) * self.speed
        self.pos[1] += math.sin(self.angle) * self.speed

        self.speed = max(0, self.speed -0.12)
        self.size = max(0, self.size -0.2)
        return not self.speed
    
    def render(self, surf, offset=(0, 0)):
        reach = [-8, 8]
        render_points = []

        for i in range(1):
            render_points.append([self.pos[0] + random.randint(reach[0], 0) - offset[0], self.pos[1] + random.randint(0, reach[1]) - offset[1]])

        for element in render_points:

            pygame.draw.circle(surf, (70, 35, 34), element, self.size)
            