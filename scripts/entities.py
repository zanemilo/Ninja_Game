import pygame

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size, velocity):
        self.game = game
        self.e_type = e_type
        self.pos = list(pos)  # any iterable becomes a list
        self.size = size
        self.velocity = [0, 0]

    def update(self, movement = (0, 0)):
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])  #enables multiple layered controls that factor into movement, input and obj velocity in this case
