# File: utils.py
# Author: Zane Deso
# Purpose: Serves currently as a convienience function toolset for use in other files/scripts.

import os

import pygame

BASE_IMG_PATH = 'data/images/'

def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert() # convert makes the image more efficient for rendering, important for performance
    img.set_colorkey((0, 0, 0))
    return img

def load_images(path):
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):  #os.listdir will take a path, and list all of the files in that path
        images.append(load_image(path + '/' + img_name)) 
    return images