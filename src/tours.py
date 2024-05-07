import pygame
from math import dist


class Fleche():
	def __init__(self):
		self.target = 0
		self.cos = ()
		
	def update_mouvement(self):
		pass
		
		
class Tour():
	def __init__(self):
		self.center_tile = ()
		self.cos_pixel = ()
		self.rayon_atk = 5
		self.hp = 1000
		self.damage = 200
		self.id = 20
		self.tower_type = None
		
	
	def spawn(self, board):
		board[self.center_tile[0]][self.center_tile[1]] = self.id
		w, h = pygame.display.get_surface().get_size()
		
		self.cos_pixel = ((self.center_tile[0]-1)*(w*1.6/100), (self.center_tile[1]-1)*(w*1.6/100))
	def targetable_minions(self, minions):
		ret = []
		for i in minions:
			if dist(i.cos, self.center_tile) <= self.rayon_atk:
				ret.append(i)
				return ret
				
		return ret
