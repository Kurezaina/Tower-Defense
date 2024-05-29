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
		""" Met à jour la position de la flèche pour l'approcher de l'ennemi ciblé"""
		x = math.cos(radians(self.rotation))*16
		y = math.sin(radians(self.rotation))*16
		self.cos = (self.cos[0] + x, self.cos[1] + y)
	def check_done(self):
		"""
		Vérifie avec une équation de disque si la flèche a atteint sa destination
		return True ou False
		"""
		
		if dist(self.cos, self.premieres_cos_cible) < 10:
			return True
		return False
		
		
		
class Tour():
	def __init__(self):
		self.center_tile = ()
		self.cos_pixel = ()
		self.rayon_atk = 20
		self.hp = 1000
		self.damage = 125
		self.id = 20
		self.tower_type = None
		self.sprite = None 
		self.arrow_img = None
		
	
	def spawn(self, board):
		"""
		Fait apparaitre la tour dans la matrice du jeu
		@param board: la matrice
		"""
		
		for c in range(3):
			for r in range(3):
				board[self.center_tile[1]-1+c][self.center_tile[0]-1+r] = self.id
		
		w, h = pygame.display.get_surface().get_size()
		
		self.cos_pixel = ((self.center_tile[0]-1)*(w*1.6/100), (self.center_tile[1]-1)*(w*1.6/100))
		
	def despawn(self, board):
		""" 
		Fait disparaitre la tour dans la matrice du jeu
		@param board: la matrice		
		"""
		for c in range(3):
			for r in range(3):
				board[self.center_tile[1]-1+c][self.center_tile[0]-1+r] = common.TILE_PLACEMENT
						
	def targetable_minions(self, minions):
		"""
		Calcule la distance entre les ennemis et la tour pour savoir si ils sont à portée d'attaque.
		@param minions: la liste d'ennemis
		return l'ennemi à portée le plus proche de l'arrivée qui sera attaqué par la touraz
		"""
		ret = []
		for i in minions:
			# Équation de disque pour savoir si l'ennemi est à portée
			if dist(i.cos, self.center_tile) <= self.rayon_atk:
				ret.append(i)
			
		if len(ret) > 0:
			# La tour doit toujours attaquer l'ennemi le plus proche de l'arrivée.
			return [min(ret, key=lambda x: dist(x.cos, (49,12)))]
		else:
			return []
		
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
		
		
	def attack(self, ennemi):
		ennemi.hp -= self.damage
		
	
class Archer(Tour):
	def __init__(self, game):
		super(Archer, self).__init__()
		self.rayon_atk = 20
		self.hp = 1000
		self.damage = 143
		self.arrow_img = game.arrow_img
		self.sprite = game.tour_img
		self.cost = 500
		

		
		
class Sorcier(Tour):
	def __init__(self, game):
		super(Sorcier, self).__init__()
		self.rayon_atk = 10
		self.rayon_aoe = 2
		self.hp = 1000
		self.damage = 200
		self.cost = 1250
		self.arrow_img = game.fireball_img
		self.sprite = game.mage_img
		
	def targetable_minions(self, minions):
		"""
		Calcule la distance entre les ennemis et la tour pour savoir si ils sont à portée d'attaque.
		@param minions: la liste d'ennemis
		Différent pour la tour de sorcier
		"""
		ret = []
		for i in minions:
			# Équation de disque pour savoir si l'ennemi est à portée
			if dist(i.cos, self.center_tile) <= self.rayon_atk:
				ret.append(i)
			
		if len(ret) > 0:
			# La tour doit toujours attaquer l'ennemi le plus proche de l'arrivée.
			center = min(ret, key=lambda x: dist(x.cos, (49,12)))
			ennemi_cos = center.cos
			ret = []
			# On attaque aussi tous les ennemis proches de l'ennemi ciblé
			for i in minions:
				if dist(i.cos, ennemi_cos) <= self.rayon_aoe:
					ret.append(i)	
			return ret	
		else:
			return []	
			
						
		
