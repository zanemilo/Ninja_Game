import math
import random
import pygame

from scripts.particle import Particle

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)  # any iterable becomes a list, for example passing a tuple -> list
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}  

        self.action = ''
        self.anim_offset = (-3, -3)
        self.flip = False
        self.set_action('idle')

        self.last_movement = [0, 0]

    def rect(self):
        """Reason for function is that we update our pos all the time and need a refreshed rect when required"""
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + '/' + self.action].copy()

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

        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True
        
        self.last_movement = movement

        self.velocity[1] = min(5, self.velocity[1] + 0.1)  # nice way of doing take the smaller number to make terminal velocity <= 5.

        if self.collisions['down'] or self.collisions['up']:  # When collision down or up, reset velodity to 0 so velocity does not persist.
            self.velocity[1] = 0

        self.animation.update()

    def render(self, surf, offset=(0, 0)):
        """Given surf param, blit the path to the current animation img at self.pos on the surf param with built in scroll offset and animating offset"""
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))

class Enemy(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'enemy', pos, size)

        self.walking = 0

    def update(self, tilemap, movement=(0, 0)):
        if self.walking:
            if tilemap.solid_check((self.rect().centerx + (-7 if self.flip else 7), self.pos[1] + 23)):  # looking 7 pixes to right or left from center, and in the ground
                if (self.collisions['right'] or self.collisions['left']):  # detects wall collisions
                    self.flip = not self.flip
                else:
                    movement = (movement[0] - 0.5 if self.flip else 0.5, movement[1])  # change movement amount based on direction enemy faces
            else:
                self.flip = not self.flip
            self.walking = max(0, self.walking - 1)
        elif random.random() < 0.01:  # if not walking, 1% chance of occuring each frame
            self.walking = random.randint(30, 120)  # number of frames to continually walk for randomly generated

        super().update(tilemap, movement=movement)

        if movement[0] != 0:
            self.set_action('run')
        else:
            self.set_action('idle')
    

class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'player', pos, size)
        self.air_time = 0
        self.jumps = 2
        self.walls_slide = False
        self.dashing = 0
         
    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement=movement)

        self.air_time += 1
        if self.collisions['down']:
            self.air_time = 0
            self.jumps = 2

        self.walls_slide = False  # Single frame switch to reset wall_slide
        if (self.collisions['right'] or self.collisions['left']) and self.air_time > 4:  # if we hit the wall on either side and we are in the air
            self.walls_slide = True
            self.velocity[1] = min(self.velocity[1], 0.5)  # Cap drop rate if wall sliding
            if self.collisions['right']:
                self.flip = False
            else:
                self.flip = True
            self.set_action('wall_slide')
        
            

        if not self.walls_slide:
            if self.air_time > 4:
                self.set_action('jump')
            elif movement[0] != 0:
                self.set_action('run')
            else:
                self.set_action('idle')

        if self.dashing > 0:
            self.dashing = max(0, self.dashing - 1)  # Pull dashing towards 0
        if self.dashing < 0:
            self.dashing = min(0, self.dashing + 1)  # Pull dashing towards 0
        if abs(self.dashing) > 50: 
            self.velocity[0] = abs(self.dashing) / self.dashing * 8  # In the first ten frames of dash, set velocity to scalar direction 
            if abs(self.dashing) == 51:
                self.velocity[0] *= 0.1  # At the end of the first ten frames, cut down on velocity (sudden stop)
            pvelocity = [abs(self.dashing) /  self.dashing * random.random() * 3, 0]
            self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=pvelocity, frame=random.randint(0, 7)))  # Stream particles
        if abs(self.dashing) in {59, 49}:  # At start and end of dash
            for i in range(20):  # create 20 particles
                angle = random.random() * math.pi * 2  # Take random angle from all angles in a circle
                speed = random.random() * 0.5 + 0.5    #  Take the cos of a random angle, and speed then
                pvelocity = [math.cos(angle) * speed, math.sin(angle) * speed]  # Generate velocity based on the angle, trig
                #  Take the cos of a random angle, and speed then 
                self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=pvelocity, frame=random.randint(0, 7)))  # Burst of particles
            

        if self.velocity[0] > 0:
            self.velocity[0] = max(self.velocity[0] - 0.1, 0)  # Pull velocity towards 0
        else:
            self.velocity[0] = min(self.velocity[0] + 0.1, 0)

    def render(self, surf, offset=(0, 0)):
        """Polymorph function to make the player invisible after first ten frames of dashing"""
        if abs(self.dashing) <= 50: #If not in first ten frames of dash in either direction
            super().render(surf, offset=offset)  # super to call parent class render function

    def jump(self):
        if self.walls_slide:
            if self.flip and self.last_movement[0] < 0:
                self.velocity[0] += 2.7  # push away from wall
                self.velocity[1] = -2.5 # wall jump
                self.air_time = 5
                self.jumps = max(0, self.jumps - 1)
                return True
            elif not self.flip and self.last_movement[0] > 0:
                self.velocity[0] -= 2.7  # push away from wall
                self.velocity[1] = -2.5 # wall jump
                self.air_time = 5
                self.jumps = max(0, self.jumps - 1)
                return True

        elif self.jumps:
            self.velocity[1] = -3
            self.jumps -= 1
            self.air_time = 5
            return True

    def dash(self):
        if not self.dashing:
            if self.flip:  # Moving left
                self.dashing = -60
            else:  # Moving Right
                self.dashing = 60
