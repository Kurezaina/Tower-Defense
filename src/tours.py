import pygame
from math import dist, degrees, atan2, radians
import math
import common


class Fleche():
	def __init__(self, cible, cos, image, screen):
		self.target = cible
		self.cos = cos
		self.premieres_cos_cible = cible.cos_pixel
		self.vector = pygame.Vector2(cible.cos_pixel[0] - cos[0], cible.cos_pixel[1] - cos[1])
		right_vec = pygame.Vector2(1, 0)
		self.rotation = right_vec.angle_to(self.vector)
		self.screen = screen
		
		self.model = pygame.transform.rotate(image, -self.rotation)
		screen.blit(self.model, cos)
		
		
	def update_mouvement(self):
		x = math.cos(radians(self.rotation))*16
		y = math.sin(radians(self.rotation))*16
		self.cos = (self.cos[0] + x, self.cos[1] + y)
		self.check_done()
	def check_done(self):
		if dist(self.cos, self.premieres_cos_cible) < 10:
			return True
		return False
		
		
		
class Tour():
	def __init__(self):
		self.center_tile = ()
		self.cos_pixel = ()
		self.rayon_atk = 10
		self.hp = 1000
		self.damage = 200
		self.id = 20
		self.tower_type = None
		
	
	def spawn(self, board):
		board[self.center_tile[1]][self.center_tile[0]] = self.id
		w, h = pygame.display.get_surface().get_size()
		
		self.cos_pixel = ((self.center_tile[0]-1)*(w*1.6/100), (self.center_tile[1]-1)*(w*1.6/100))
	def targetable_minions(self, minions):
		ret = []
		for i in minions:
			if dist(i.cos, self.center_tile) <= self.rayon_atk:
				ret.append(i)
				return ret
			
		return ret
		
	def check_placable(self, board):
		""""
		Vérifie si la tour est plaçable sur la matrice en fonction de ses coordonnées
		@param board: la matrice
		return: True ou False
		"""
		
		for c in range(3):
			for r in range(3):
				if board[self.center_tile[1]-1+c][self.center_tile[0]-1+r] != common.TILE_PLACEMENT:
					return False
		
		return True 
						
		
