#!/usr/bin/env python

import pygame
import os
from math import sqrt

import pygame_gui as pgu
import itertools as it
# Pour les maps de tiled
from pytmx import load_pygame
from pygame_gui.elements import UITextBox, UIButton
from pygame_gui.core import ObjectID
from gmap import *

dossier = os.path.dirname(os.path.realpath(__file__))
Game = 0
pygame.display.set_caption("Tower Défense")



		
class Tour():
	def __init__(self):
		self.center_tile = ()
		self.hp = 1000
		self.tower_type = None

		
class Minion():
	def __init__(self):
		self.tile = ()
		self.hp = 1000
		self.minion_type = None


class MainGame():
	def __init__(self):
 
		self.current_scale = 1
		
		self.board = []
		for i in range(200):
			self.board.append([0]*200)
		self.enemies = []
		self.towers = []
		
		 
		# 1 = Ennemi, 0 = Joueur
		self.current_turn = 1

		#position sur la minimap
		self.pos_x_minimap = 0
		self.pos_y_minimap = 0
		self.running = True

		self.new_x_off = 0
		self.new_y_off = 0
		
		# Une clock
		self.clock = pygame.time.Clock()
		
		# Un pygame.screen
		self.screen = 0
		
		# On place la cam au centre de la map
		w, h = pygame.display.get_surface().get_size()

		self.mapdata = Map((50,50), 32, (100,100))
		self.x_off = -self.mapdata.get_center()[0]*32 + w/2
		self.y_off = -self.mapdata.get_center()[1]*32+ h/2
			
		self.map = load_pygame(os.path.join(dossier,"../Map/Map/Map.tmx"))


		self.gold = 0
		# UI
		
		self.uimanager = pgu.UIManager((w, h), os.path.join(dossier, "theme.json"))
		self.gold_rect = pygame.Rect((0, 0), (80, 30))
		self.gold_rect.topleft = (30, 10)
		self.goldcounter = UITextBox(relative_rect=self.gold_rect, html_text=str(self.gold))
		
		"""
		
		self.reputation_rect = pygame.Rect((0, 0), (80, 30))
		self.reputation_rect.topleft = (130, 10)		
		self.reputationcounter = UITextBox(relative_rect=self.reputation_rect, html_text=(str(self.reputation*100) + "%"))

		self.test_rect = pygame.Rect((0, 0), (80, 30))
		self.test_rect.topleft = (230, 10)
		self.testcounter = UITextBox(relative_rect=self.test_rect, html_text=(str(self.mask_wear)))
		"""

		
	# Mettre à jour les compteurs (goldité, réputation, etc...)
	def update_counters(self):
		gold_colour = ""
		if self.gold < 0:
			# Rouge
			gold_colour = "#FF0000"
		else:
			# Blanc
			gold_colour = "#FFFFFF"
			
		rep_colour = ""
		
		html_gold = """<font color="{colour}">{value}</font>""".format(colour=gold_colour, value=str(self.gold))
		
		self.goldcounter.set_text(html_gold)
		return
		
		
		
		
	def loop(self):

		# On charge la map
		w, h = pygame.display.get_surface().get_size() 			
		surface = pygame.Surface((self.mapdata.tilewidth*self.mapdata.tiled_map_size[0],self.mapdata.tilewidth*self.mapdata.tiled_map_size[1])).convert()
		for layer in self.map.visible_layers:
			for x, y, img in layer.tiles():

				surface.blit(img, (x * self.map.tilewidth,
									   y * self.map.tileheight ))

		
		grid_surface = pygame.Surface((self.mapdata.tilewidth*self.mapdata.tiled_map_size[0],self.mapdata.tilewidth*self.mapdata.tiled_map_size[1]), pygame.SRCALPHA, 32).convert_alpha()
		grid_surface.set_alpha(64)
		cordx = 0
		cordy = 0
		for i in range(self.mapdata.tiled_map_size[1]):
			for i in range(self.mapdata.tiled_map_size[0]):
				rect = pygame.Rect(cordx, cordy, 64, 64)
				pygame.draw.rect(grid_surface, (0,0,0),rect, 1)
				cordx += 64
			cordx = 0
			cordy += 64		
			
		surface.blit(grid_surface, (0,0))
		surface = pygame.transform.smoothscale(surface, (w, h))
				
		
		# On remplit le plateau avec les tiles qui seront traversable par les troupes ennemies.
		for layer in self.map.visible_layers:
			if layer.name == "Chemin":
				for x, y, gid in layer.tiles():
					x = mapclass.tiled_cords_to_pixels(x)
					y = mapclass.tiled_cords_to_pixels(y)
					
					self.board[x][y] = 1
			elif layer.name == "Points":
				for x, y, gid in layer.tiles():
					x = mapclass.tiled_cords_to_pixels(x)
					y = mapclass.tiled_cords_to_pixels(y)
					
					self.board[x][y] = 2					
		
		while self.running:
			dt = self.clock.tick(30)/1000	
			Keys = pygame.key.get_pressed()					
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False
					pygame.quit()

			self.screen.fill((0,0,0))


			self.screen.blit(surface, (0,0))
			
			w, h = pygame.display.get_surface().get_size()			

			self.update_counters()
			self.uimanager.update(dt)	
												
			self.uimanager.draw_ui(self.screen)

			pygame.display.flip()
			
			
						
if __name__ == "__main__":
	pygame.init()
	
	screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
	pygame.display.toggle_fullscreen()
	
	running = True
	while running:

		Game = MainGame()
		Game.screen = screen
		Game.loop()
	
	pygame.quit()
	
	
	
	
	
