import pygame

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.e_type = e_type
        self.pos = list(pos)  # any iterable becomes a list, for example passing a tuple -> list
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}  

    def rect(self):
        """Reason for function is that we update our pos all the time and need a refreshed rect when required"""
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def update(self, tilemap, movement = (0, 0)):
        """Called to update movement and detect collisions"""
        # Which direction an entity just collided with
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

        # Enables multiple layered controls that factor into movement, input and obj velocity in this case
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])  

        self.pos[0] += frame_movement[0]  # X AXIS
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):  # All nearby tiles
            if entity_rect.colliderect(rect):  # Detect Collision between the two
                if frame_movement[0] > 0:  # Moving to the right
                    entity_rect.right = rect.left  # Snap the entity to the leftside of collided tile
                    self.collisions['right'] = True
                if frame_movement[0] < 0:  # Moving Left
                    entity_rect.left = rect.right  # Snap the entity to the rightside of collided tile
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x  # Update entity pos to match rect pos

        self.pos[1] += frame_movement[1]  # Y AXIS
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):  # All nearby tiles
            if entity_rect.colliderect(rect):  # Detect Collision between the two
                if frame_movement[1] > 0:  # Moving downward
                    entity_rect.bottom = rect.top  # Snap the entity to the top of collided tile
                    self.collisions['down'] = True
                if frame_movement[1] < 0:  # Moving upward
                    entity_rect.top = rect.bottom  # Snap the entity to the bottom of collided tile
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y  # Update entity pos to match rect pos

        self.velocity[1] = min(5, self.velocity[1] + 0.1)  # nice way of doing take the smaller number to make terminal velocity <= 5.

    def render(self, surf):
        """Given surf param, blit the path to the 'player' img at self.pos on the surf param"""
        surf.blit(self.game.assets['player'], self.pos)
