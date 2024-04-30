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


class MainGame():
	def __init__(self):
 

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

		
	def load_current_event(self):
		self.event_text_box.show()
		
		self.event_text_box.set_text("""<font color="#FFFFFF">{value}</font>""".format(value=self.current_event.current_node.text[self.current_event.current_text_phase]))	
		self.event_text_box.set_active_effect(pgu.TEXT_EFFECT_TYPING_APPEAR, params={'time_per_letter': 0.025})		
		self.current_event.loaded = True
		
		
	def show_options(self):
		return 
		w, h = pygame.display.get_surface().get_size()
		opts = len(self.current_event.current_node.options)
		# On fait le layout des boutons 
		rects = []
		
		top = opts*h/20
		cords = self.player.cords
		
		for i in range(opts):
		
			rect = pygame.Rect((0,0), (-1, h/20))
			rect.center = (0, cords[1]-(top-i*h/20))
			rects.append(rect)

			choice = UIButton(anchors={'centerx': 'centerx'}, relative_rect=rect, text=self.current_event.current_node.options[i], manager=self.uimanager,object_id=ObjectID(class_id="@dialogbtn"))
				
			self.option_btns.append(choice)
		
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

		while self.running:
			dt = self.clock.tick(30)/1000	
			Keys = pygame.key.get_pressed()					
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False
					pygame.quit()

			self.screen.fill((0,0,0))


			self.screen.blit(surface, (self.x_off,self.y_off))
			
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
	
	
	
	
	
