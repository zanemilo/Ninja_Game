import sys

import pygame

class Game:
    def __init__(self) :
        
        pygame.init()

        pygame.display.set_caption("Ninja Game")  # Name of game, appears top lef tof window
        self.screen = pygame.display.set_mode((640, 480)) # screen obj. Resolution of window

        self.clock = pygame.time.Clock()

        self.img = pygame.image.load('data/images/clouds/cloud_1.png')  # Load a img obj, this is a cloud
        self.img_pos = [160, 260]
        self.movement = [False, False]

    def run(self):
        while True:
            self.screen.fill((14, 219, 248))  # reset screen with background color (R, B, G)
            self.img_pos[1] += (self.movement[1] - self.movement[0]) * 5  # y value += 1 if upkey is down, -1 if downkey is down, 0 otherwise. speed multiplier is last int
            self.screen.blit(self.img, self.img_pos)  # draw/blit img onto screen
            
            for event in pygame.event.get():  # handles all kinds of events, including key press, mouse movement etc.
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.movement[0] = True
                    if event.key == pygame.K_DOWN:
                        self.movement[1] = True   
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.movement[0] = False
                    if event.key == pygame.K_DOWN:
                        self.movement[1] = False

            pygame.display.update()
            self.clock.tick(60)

Game().run()