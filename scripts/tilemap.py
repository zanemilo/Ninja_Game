class Tilemap:
    def __init__(self, tile_size=16):
        self.tile_size = tile_size  
        self.tilemap = {}  # Every tile is on a square grid
        self.offgrid_tiles = []  # Tiles for off grid, all over the place

        # Concatonates location based on for loop i with fixed position of 10 as denoted by ';10', 
        # this location contains a dict that holds informaiton about the tile such as type, variant, and position.
        for i in range(10):
            self.tilemap[str(3 + i) + ';10'] = {'type': 'grass', 'variant': 1, 'pos': (3 + i, 10)}  # 3-10 on X, 10 on Y. Horizontal line of grass tiles.
            self.tilemap['10;' + str(5 + i)] = {'type': 'stone', 'variant': 1, 'pos': (10, 5 + i)}  # 10 on X, 5-15 on Y. Vertical line of stone tiles. 
            
        