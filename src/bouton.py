import pygame
import os
import common
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

		surf = pygame.Surface((self.rectangle.w, self.rectangle.h)).convert_alpha()
		surf.fill(self.color)


		if self.sprite:
			surf.blit(self.sprite, (0, 0))		
			
		screen.blit(surf, (self.x, self.y))
		
		
class Tour_selection_bouton(Button):
	def __init__(self, x,y,w,h, tower=Archer, sprite=None, color=(255,255,255)):
		super(Tour_selection_bouton, self).__init__(x,y,w,h, color=color, sprite=None)
		self.sprite = sprite
		self.font = pygame.font.Font(os.path.join(common.font_dossier, "Montserrat-Regular.ttf"))
		print(self.color)
	def render(self, screen):

		surf = pygame.Surface((self.rectangle.w, self.rectangle.h)).convert_alpha()
		surf.fill(self.color)
		
		cout = self.tower(common.game).cost
		
		# Texte de couleur rouge si on a pas les thunes
		text_color = (125,0,0) if common.game.gold < cout else (255,255,255)
		
		if self.sprite:
			surf.blit(self.sprite, (0, 0))		
			surf.blit(self.font.render(str(cout), True, text_color), (0,80))
			
		screen.blit(surf, (self.x, self.y))

class Archer_build_selection_bouton(Tour_selection_bouton):
	def __init__(self,x,y,w,h, tower=Archer, color=None, sprite=None):
		super(Archer_build_selection_bouton, self).__init__(x,y,w,h, color=color, sprite=sprite)
		self.tower = tower
		
		
	def click(self, game):
		if not self.toggled:
			game.tower_to_place = self.tower
			self.toggled = True
		else:
			game.tower_to_place = None
			self.toggled = False


class Sorcier_build_selection_bouton(Tour_selection_bouton):
	def __init__(self,x,y,w,h, tower=Sorcier, color=None, sprite=None):
		super(Sorcier_build_selection_bouton, self).__init__(x,y,w,h, color=color, sprite=sprite)
		self.tower = tower
		
		
	def click(self, game):
		if not self.toggled:
			game.tower_to_place = self.tower
			self.toggled = True
		else:
			game.tower_to_place = None
			self.toggled = False

