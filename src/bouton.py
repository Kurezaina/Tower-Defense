import pygame
from tours import *
class Button():
	def __init__(self,x,y,w,h, sprite=None, color=(255,255,255)):
		"""
		Créé un bouton.
		@param x et y: Les coordonnées du bouton (relative à l'écran)
		@param w et h : Longueur et hauteur du bouton
		"""
		self.x= x
		self.y = y
		self.w = w
		self.h = h
		
		self.rectangle = pygame.Rect(x,y,w,h)
		self.sprite = pygame.transform.scale(sprite,(w,h)) if sprite else None
		self.color = color
		self.toggled = False
        
		
	def click(self, game):
		"""
		Fonction exécutée quand le self.rectangle est cliqué (le bouton quoi)
		@param game: objet MainGame
		"""
		
	def render(self, screen):
		"""Fonction qui affiche le bouton sur l'écran
		@param screen: l'écran
		"""
		pygame.draw.rect(screen, self.color, self.rectangle)
		if self.sprite:
			screen.blit(self.sprite, (self.x, self.y))
		

class Tour_build_selection_bouton(Button):
	def __init__(self,x,y,w,h, tower=Tour, color=None, sprite=None):
		super(Tour_build_selection_bouton, self).__init__(x,y,w,h, color=color, sprite=sprite)
		self.tower = tower
		
		
	def click(self, game):
		if not self.toggled:
			game.tower_to_place = self.tower
			self.toggled = True
		else:
			game.tower_to_place = None
			self.toggled = False

		print("Selecting tower")
