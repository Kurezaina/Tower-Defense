import pygame
from tours import *
class Button():
	def __init__(self,x,y,w,h):
		"""
		Créé un bouton.
		@param x et y: Les coordonnées du bouton (relative à l'écran)
		@param w et h : Longueur et hauteur du bouton
		"""
		self.rectangle = pygame.Rect(x,y,w,h)
		self.color = None
		self.toggled = False
		
	def click(self, game):
		"""
		Fonction exécutée quand le self.rectangle est cliqué (le bouton quoi)
		@param game: objet MainGame
		"""
		

class Tour_build_selection_bouton(Button):
	def __init__(self,x,y,w,h, tower=Tour):
		super(Tour_build_selection_bouton, self).__init__(x,y,w,h)
		self.tower = tower
		
		
	def click(self, game):
		if not self.toggled:
			game.tower_to_place = self.tower
			self.toggled = True
		else:
			game.tower_to_place = None
			self.toggled = False

		print("Selecting tower")
