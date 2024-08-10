import sys

import random
import math
import pygame

from scripts.entities import PhysicsEntity, Player
from scripts.utils import load_image, load_images, Animation
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds
from scripts.particle import Particle

class Game:
    """ Game obj required for encapsulating game functions, attributes and variables. Thereby presenting cleaner code, following better practices, simplifying troubleshooting and more."""
    def __init__(self) : 
        pygame.init()

        pygame.display.set_caption("Ninja Game")  # Name of game, appears top lef tof window
        self.screen = pygame.display.set_mode((640, 480))  # screen obj. Resolution of window
        self.display = pygame.Surface((320, 240))  # the actual display that you render onto, Surface is an empty image, all black by default
        
        self.clock = pygame.time.Clock()

        self.movement = [False, False]  # Boolean representation of if Left, Right keys respectively are being pressed/held or not.

        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone') ,
            'player': load_image('entities/player.png'),
            'background': load_image('background.png'),
            'clouds': load_images('clouds'),
            'player/idle': Animation(load_images('entities/player/idle'), img_dur=6),
            'player/run': Animation(load_images('entities/player/run'), img_dur=4),
            'player/jump': Animation(load_images('entities/player/jump')),
            'player/slide': Animation(load_images('entities/player/slide')),
            'player/wall_slide': Animation(load_images('entities/player/wall_slide')),
            'particle/leaf': Animation(load_images('particles/leaf'), img_dur=20, loop=False)

        }

        self.clouds = Clouds(self.assets['clouds'], count=16)

        self.player = Player(self, pos=(50, 50), size=(8, 15))  # instantiate player obj for use in game/run function in main.

        self.tilemap = Tilemap(self, tile_size=16)  # self to pass in game reference to then instantiate Tilemap with default size 16
        self.tilemap.load("map.json")

        self.leaf_spawners = []
        for tree in self.tilemap.extract([('large_decor', 2)], keep=True):
            self.leaf_spawners.append(pygame.Rect(4 + tree['pos'][0], 4 + tree['pos'][1], 23, 13))  # Taking the pos of the tile, and area of tree img to spawn leaves with offset of 4 from top left
        
        self.particles = []

        self.scroll = [0, 0]  # camera location

    def run(self):
        while True:
            self.display.blit(self.assets['background'], (0, 0))


            # since orientation of camera is based on top left, subtract part of screen size to centerplayer then /30 will ramp slow/speed up depending on distance
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) /30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) /30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            for rect in self.leaf_spawners:
                if random.random() * 49999 < rect.width * rect.height:  # controls rate of particle span makes sure it is proportional to size of object (ie. bigger trees)
                    pos = (rect.x + random.random() * rect.width, rect.y + random.random() * rect.height)  # get random number within the bounds of the rect
                    self.particles.append(Particle(self, 'leaf', pos, velocity=[-0.1, 0.3], frame=random.randint(0, 20)))  # Spawns particle leaf by adding new leaf instance to particles list

            self.clouds.update()
            self.clouds.render(self.display, offset=render_scroll)

            self.tilemap.render(self.display, offset=render_scroll)  # each call, render tile map

            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))  # each call, update  player movement bools, accounting for if both (Left and Right keys) are being pressed adding to 0 (False), and for now we are not allowing y movement.
            self.player.render(self.display, offset=render_scroll)  # each call, render player

            for particle in self.particles.copy():  # using copy due to removing during iteration
                kill = particle.update()
                particle.render(self.display, offset=render_scroll)  # Render the leaf particles
                if particle.type == 'leaf':
                    particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.3
                if kill:
                    self.particles.remove(particle)
            
            for event in pygame.event.get():  # handles all kinds of events, including key press, mouse movement etc.
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        self.player.jump()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))  # Render display onto screen (window), transform the size of display to screen (get its size)
            pygame.display.update()
            self.clock.tick(60)

Game().run()