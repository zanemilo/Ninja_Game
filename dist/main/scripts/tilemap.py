import json

import pygame
AUTOTILE_MAP = {  # rules used for autotiling
    tuple(sorted([(1, 0), (0, 1)])): 0,
    tuple(sorted([(1, 0), (0, 1), (-1, 0)])): 1,
    tuple(sorted([(-1, 0), (0, 1)])): 2,
    tuple(sorted([(-1, 0), (0, -1), (0, 1)])): 3,
    tuple(sorted([(-1, 0), (0, -1)])): 4,
    tuple(sorted([(-1, 0), (0, -1), (1, 0)])): 5,
    tuple(sorted([(1, 0), (0, -1)])): 6,
    tuple(sorted([(1, 0), (0, -1), (0, 1)])): 7,
    tuple(sorted([(1, 0), (-1, 0), (0, 1), (0, -1)])): 8,
}

NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)] # All of the offsets to calc/help look up 9 tiles around the player for physics
PHYSICS_TILES = {'grass', 'stone'}  # This is a set (a dict without the ": 0" value pair) it is not allowed to have dupes and has faster lookup time than lists
AUTOTILE_TYPES = {'grass', 'stone'}  # This is the CONST for autotiling tile types

class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size  
        self.tilemap = {}  # Every tile is on a square grid
        self.offgrid_tiles = []  # Tiles for off grid, all over the place

    def extract(self, id_pairs, keep=False):
        """Take a tile types and tell us where they are and info about them. Can be used for removing things later"""
        matches = []
        for tile in self.offgrid_tiles.copy():
            if (tile['type'], tile['variant']) in id_pairs:
                matches.append(tile.copy())
                if not keep:
                    self.offgrid_tiles.remove(tile)
        
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            if (tile['type'], tile['variant']) in id_pairs:
                matches.append(tile.copy())
                matches[-1]['pos'] = matches[-1]['pos'].copy()  # take copy to refer to clean copy, otherwise risk nested data
                matches[-1]['pos'][0] *= self.tile_size  # changing pos of tile we are referencing in pixels to grid
                matches[-1]['pos'][1] *= self.tile_size
                if not keep:
                    del self.tilemap[loc]

        return matches
           
    def tile_around(self, pos):
        """Return the 9 tiles surronding the pos given, use NEIGHBOR_OFFSETS const to calc the 9 surrnding by adding offset to pos coords."""
        tiles = []  # tiles to be returned
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))  # convert pixel pos into grid pos
        for offset in NEIGHBOR_OFFSETS:
            check_loc = str(tile_loc[0] + offset[0]) + ";" + str(tile_loc[1] + offset[1]) # adding offsets to base location
            if check_loc in self.tilemap:  # check to see if the tile location is actually in tilemap
                tiles.append(self.tilemap[check_loc])  # if so, add it to tiles to be returned
        return tiles
    
    def save(self, path):
        """Saves tilemap editors current tile placements into json file"""
        f = open(path, 'w')  # open file
        json.dump({'tilemap': self.tilemap, 'tile_size': self.tile_size, 'offgrid': self.offgrid_tiles}, f)  # dump specified contents into file
        f.close()

    def load(self, path):
        """Loads tilemap"""
        f = open(path, 'r')
        map_data = json.load(f)
        f.close()

        self.tilemap = map_data['tilemap']
        self.tile_size = map_data['tile_size']
        self.offgrid_tiles = map_data['offgrid']
    
    def solid_check(self, pos):
        tile_loc = str(int(pos[0] // self.tile_size)) + ';' + str(int(pos[1] // self.tile_size))  # gives tile loc, transform pixels to tile system
        if tile_loc in self.tilemap:
            if self.tilemap[tile_loc]['type'] in PHYSICS_TILES:
                return self.tilemap[tile_loc]
    
    def physics_rects_around(self, pos):
        rects = []  # rects to be returned
        for tile in self.tile_around(pos):  # get the tiles around the param pos
            if tile['type'] in PHYSICS_TILES:  # from the detected tiles around pos param that show up in const
                # add a non-rendered rect with the detected tiles position and size scaled appropriately <- another way to see it, return nearby detected tiles of PHYSICS_TILES type as Rectangles
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))  
        return rects
    
    def autotile(self):
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            neighbors = set()
            for shift in [(1, 0), (-1, 0), (0, -1), (0, 1)]:
                check_loc = str(tile['pos'][0] + shift[0]) + ';' + str(tile['pos'][1] +shift[1])
                if check_loc in self.tilemap:
                    if self.tilemap[check_loc]['type'] == tile['type']:
                        neighbors.add(shift)
            neighbors = tuple(sorted(neighbors))
            if (tile['type'] in AUTOTILE_TYPES) and (neighbors in AUTOTILE_MAP):
                tile['variant'] = AUTOTILE_MAP[neighbors]

    def render(self, surf, offset=(0, 0)):
        for tile in self.offgrid_tiles:
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))

        for x in range(offset[0] // self.tile_size, (offset[0] + surf.get_width()) // self.tile_size + 1):  # divde offset by tile size finding top left tile, find right edge of screen (off by one error)
            for y in range(offset[1] // self.tile_size, (offset[1] + surf.get_height()) // self.tile_size + 1):
                loc = str(x) + ';' + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[-1]))
        

    