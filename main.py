import sys

import pygame

from scripts.entities import PhysicsEntity
from scripts.utils import load_image, load_images
from scripts.tilemap import Tilemap

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
            'player': load_image('entities/player.png')
        }

        print(self.assets )

        self.player = PhysicsEntity(self, e_type='player', pos=(50, 50), size=(8, 15))  # instantiate player obj for use in game/run function in main.

        self.tilemap = Tilemap(tile_size=16)  # instantiate Tilemap with default size 16


    def run(self):
        while True:
            self.display.fill((14, 219, 248))  # each call, set screen with background color (R, B, G)

            self.tilemap.render(self.display)  # each call, render tile map

            self.player.update((self.movement[1] - self.movement[0], 0))  # each call, update  player movement bools, accounting for if both (Left and Right keys) are being pressed adding to 0 (False), and for now we are not allowing y movement.
            self.player.render(self.display)  # each call, render player
            
            for event in pygame.event.get():  # handles all kinds of events, including key press, mouse movement etc.
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True   
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))  # Render display onto screen (window), transform the size of display to screen (get its size)
            pygame.display.update()
            self.clock.tick(60)

Game().run()