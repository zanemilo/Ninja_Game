NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)] # All of the offsets to calc/help look up 9 tiles around the player for physics

class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size  
        self.tilemap = {}  # Every tile is on a square grid
        self.offgrid_tiles = []  # Tiles for off grid, all over the place

        # Concatonates location based on for loop i with fixed position of 10 as denoted by ';10', 
        # this location contains a dict that holds informaiton about the tile such as type, variant, and position.
        for i in range(10):
            self.tilemap[str(3 + i) + ';10'] = {'type': 'grass', 'variant': 1, 'pos': (3 + i, 10)}  # 3-10 on X, 10 on Y. Horizontal line of grass tiles.
            self.tilemap['10;' + str(5 + i)] = {'type': 'stone', 'variant': 1, 'pos': (10, 5 + i)}  # 10 on X, 5-15 on Y. Vertical line of stone tiles. 
            
    def tile_around(self, pos):
        """Return the 9 tiles surronding the pos given, use NEIGHBOR_OFFSETS const to calc the 9 surrnding by adding offset to pos coords."""
        tiles = []  # tiles to be returned
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))  # convert pixel pos into grid pos
        for offset in NEIGHBOR_OFFSETS:
            check_loc = str(tile_loc[0] + offset[0]) + ";" + str(tile_loc[1] + offset[1]) # adding offsets to base location
            if check_loc in self.tilemap:  # check to see if the tile location is actually in tilemap
                tiles.append(self.tilemap[check_loc])  # if so, add it to tiles to be returned
        return tiles

    def render(self, surf):
        for tile in self.offgrid_tiles:
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos']))
        
        for loc in self.tilemap: # Every tile is on a square grid
            tile = self.tilemap[loc]
            # render the tile onto param surf, position of tile is based on dict position in tilemap then multiplies them by tile_size attribute
            surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size ))

    