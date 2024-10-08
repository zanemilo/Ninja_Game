import sys

import pygame

from scripts.utils import load_images
from scripts.tilemap import Tilemap

RENDER_SCALE = 2.0  # Determines multiplicative size of each pixel


class Editor:
    """ Game obj required for encapsulating game functions, attributes and variables. Thereby presenting cleaner code, following better practices, simplifying troubleshooting and more."""
    def __init__(self) : 
        pygame.init()

        pygame.display.set_caption("Editor")  # Name of window, appears top lef tof window
        self.screen = pygame.display.set_mode((640, 480))  # screen obj. Resolution of window
        self.display = pygame.Surface((320, 240))  # the actual display that you render onto, Surface is an empty image, all black by default
        
        self.clock = pygame.time.Clock()

        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'spawners': load_images('tiles/spawners'),
        }

        self.movement = [False, False, False, False]  # Boolean representation of if Left, Right, UP and Down keys respectively are being pressed/held or not.

        self.tilemap = Tilemap(self, tile_size=16)  # self to pass in game reference to then instantiate Tilemap with default size 16
        try:
            self.tilemap.load('map.json')
        except FileNotFoundError:
            pass
        
        self.scroll = [0, 0]  # camera location
        self.scroll_speed = 3

        self.tile_list = list(self.assets)  # convert assets into a list
        self.tile_group = 0  
        self.tile_variant = 0  

        self.clicking = False
        self.right_clicking = False
        self.shift = False
        self.ongrid = True

    def run(self):
        while True:
            self.display.fill((0, 0, 0))  # black background

            self.scroll[0] += (self.movement[1] - self.movement[0]) * self.scroll_speed  # X Axis, camera movement.
            self.scroll[1] += (self.movement[3] - self.movement[2]) * self.scroll_speed  # Y Axis, camera movement. Mult by 2 to increase speed
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))  # truncated version of our scroll

            self.tilemap.render(self.display, offset=render_scroll)

            current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()  # copy is to keep alpha channel
            current_tile_img.set_alpha(100)  # set it so the img is partiall transparent

            mpos = pygame.mouse.get_pos()  # provides pixel coords of mouse with respect to window
            mpos = (mpos[0] / RENDER_SCALE, mpos[1] / RENDER_SCALE)
            tile_pos = (int((mpos[0] + self.scroll[0])  // self.tilemap.tile_size), int((mpos[1] + self.scroll[1]) // self.tilemap.tile_size))  # Provides coords of mouse in terms of tile system

            if self.ongrid:
                # Scale to pixel coords, displays preview of tiles to be place snapped ot gird
                self.display.blit(current_tile_img, (tile_pos[0] * self.tilemap.tile_size -  self.scroll[0], tile_pos[1] * self.tilemap.tile_size - self.scroll[1]))
            else:
                  # When ongrid toggled, switch to just mpos
                  self.display.blit(current_tile_img, mpos)

            if self.clicking and self.ongrid:
                                    # converts index selection into str name for the group
                self.tilemap.tilemap[str(tile_pos[0]) + ';' + str(tile_pos[1])] = {'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': tile_pos}
            if self.right_clicking:
                tile_loc = str(tile_pos[0]) + ';' + str(tile_pos[1])
                if tile_loc in self.tilemap.tilemap:
                    del self.tilemap.tilemap[tile_loc]  # tilemap attribute of the tilemap object (tilemap.tilemap)
                for tile in self.tilemap.offgrid_tiles.copy():
                    tile_img = self.assets[tile['type']][tile['variant']]
                    tile_r = pygame.Rect(tile['pos'][0] - self.scroll[0], tile['pos'][1] - self.scroll[1], tile_img.get_width(), tile_img.get_height())  # Convert world space into screen space
                    if tile_r.collidepoint(mpos):
                        self.tilemap.offgrid_tiles.remove(tile)

            self.display.blit(current_tile_img, (5, 5))
            
            for event in pygame.event.get():  # handles all kinds of events, including key press, mouse movement etc.
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True
                        if not self.ongrid:
                            self.tilemap.offgrid_tiles.append({'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': (mpos[0] + self.scroll[0], mpos[1] + self.scroll[1])})
                    if event.button == 3:
                        self.right_clicking = True
                    if self.shift:
                        if event.button == 4:
                            self.tile_variant = (self.tile_variant - 1) % len(self.assets[self.tile_list[self.tile_group]])  # loops over variants of current tile
                        if event.button == 5:
                            self.tile_variant = (self.tile_variant + 1) % len(self.assets[self.tile_list[self.tile_group]])
                    else:
                        if event.button == 4:
                            self.tile_group = (self.tile_group - 1) % len(self.tile_list)  # loops over the list up to length then back to 0
                            self.tile_variant = 0  # if you change the tile you are looking at, start at first tile
                        if event.button == 5:
                            self.tile_group = (self.tile_group + 1) % len(self.tile_list)
                            self.tile_variant = 0
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                    if event.button == 3:
                        self.right_clicking = False


                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_w:
                        self.movement[2] = True
                    if event.key == pygame.K_s:
                        self.movement[3] = True
                    if event.key == pygame.K_g:
                        self.ongrid = not self.ongrid
                    if event.key == pygame.K_t:
                        self.tilemap.autotile()
                    if  event.key == pygame.K_o:
                        self.tilemap.save('map.json')
                    if event.key == pygame.K_LSHIFT:
                        self.shift = True
                        self.scroll_speed += 2
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False
                    if event.key == pygame.K_w:
                        self.movement[2] = False
                    if event.key == pygame.K_s:
                        self.movement[3] = False
                    if event.key == pygame.K_LSHIFT:
                        self.shift = False
                        self.scroll_speed = 3

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))  # Render display onto screen (window), transform the size of display to screen (get its size)
            pygame.display.update()
            self.clock.tick(60)

Editor().run()