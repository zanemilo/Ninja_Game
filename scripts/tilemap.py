import pygame

NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)] # All of the offsets to calc/help look up 9 tiles around the player for physics
PHYSICS_TILES = {'grass', 'stone'}  # This is a set (a dict without the ": 0" value pair) it is not allowed to have dupes and has faster lookup time than lists

class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size  
        self.tilemap = {}  # Every tile is on a square grid
        self.offgrid_tiles = []  # Tiles for off grid, all over the place
           
    def tile_around(self, pos):
        """Return the 9 tiles surronding the pos given, use NEIGHBOR_OFFSETS const to calc the 9 surrnding by adding offset to pos coords."""
        tiles = []  # tiles to be returned
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))  # convert pixel pos into grid pos
        for offset in NEIGHBOR_OFFSETS:
            check_loc = str(tile_loc[0] + offset[0]) + ";" + str(tile_loc[1] + offset[1]) # adding offsets to base location
            if check_loc in self.tilemap:  # check to see if the tile location is actually in tilemap
                tiles.append(self.tilemap[check_loc])  # if so, add it to tiles to be returned
        return tiles
    
    def physics_rects_around(self, pos):
        rects = []  # rects to be returned
        for tile in self.tile_around(pos):  # get the tiles around the param pos
            if tile['type'] in PHYSICS_TILES:  # from the detected tiles around pos param that show up in const
                # add a non-rendered rect with the detected tiles position and size scaled appropriately <- another way to see it, return nearby detected tiles of PHYSICS_TILES type as Rectangles
                rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))  
        return rects

    def render(self, surf, offset=(0, 0)):
        for tile in self.offgrid_tiles:
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] - offset[0], tile['pos'][1] - offset[1]))

        for x in range(offset[0] // self.tile_size, (offset[0] + surf.get_width()) // self.tile_size + 1):  # divde offset by tile size finding top left tile, find right edge of screen (off by one error)
            for y in range(offset[1] // self.tile_size, (offset[1] + surf.get_height()) // self.tile_size + 1):
                loc = str(x) + ';' + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[-1]))
        

    