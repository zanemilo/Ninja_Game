import pygame

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.e_type = e_type
        self.pos = list(pos)  # any iterable becomes a list, for example passing a tuple -> list
        self.size = size
        self.velocity = [0, 0]

    def update(self, movement = (0, 0)):
        """Enables multiple layered controls that factor into movement, input and obj velocity in this case"""
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])  

        self.pos[0] += frame_movement[0] 
        self.pos[1] += frame_movement[1]

    def render(self, surf):
        """Given surf param, blit the path to the 'player' img at self.pos on the surf param"""
        surf.blit(self.game.assets['player'], self.pos)
