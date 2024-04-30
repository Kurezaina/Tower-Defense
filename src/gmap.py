class Map():
        def __init__(self, sp, tw, tms):
                self.spawnpoint = sp
                self.tilewidth = tw
                self.tiled_map_size = tms
        # Convertit des coordonnées sur tiled en coordonnées en pixels pour pygame.
        def tiled_cords_to_pixels(self,tc):
                return tc*self.tilewidth

        # Retourne le centre de la map en cos tiled.
        def get_center(self):
                return (self.tiled_map_size[0]/2, self.tiled_map_size[1]/2)


