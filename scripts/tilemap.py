class Tilemap:
    def __init__(self, tile_size=16):
        self.tile_size = tile_size  
        self.tilemap = {}  # Every tile is on a square grid
        self.offgrid_tiles = []  # Tiles for off grid, all over the place

        for i in range(10):
            self.tilemap[str(3 + i) + ';10'] = {'type': 'grass', 'variant': 1, 'pos': (3 + i, 10)}
        