import pygame

BASE_IMG_PATH = 'data/images/'

def load_image(path):
    img = pygame.load_image(BASE_IMG_PATH + path).convert() # convert makes the image more efficient for rendering, important for performance
    img.set_colorkey((0, 0, 0))
    return img