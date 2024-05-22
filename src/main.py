#!/usr/bin/env python

import pygame
import os
from math import sqrt, dist, floor
import operator

import pygame_gui as pgu
import itertools as it
# Pour les maps de tiled
from pytmx import load_pygame

from ennemi import *
from tours import *
import common

from pygame_gui.elements import UITextBox, UIButton
from pygame_gui.core import ObjectID
from gmap import *
from graphe import *
from ennemi import Vague, Minion
from bouton import *

dossier = os.path.dirname(os.path.realpath(__file__))
Game = 0
pygame.display.set_caption("Tower Défense")

def pixels_to_tile(pixels):
	return int(pixels/common.scale_factor)


class MainGame():
	def __init__(self):

		# Une liste des boutons pour tous les check quand on clique
		self.boutons = []
		
		# Type de tour actuellement sélectionné pour être placé
		self.tower_to_place = None

		self.current_scale = 1
		self.board = []
		# Graphes chemins
		self.graphe_chemin_1 = None
		self.graphe_chemin_3 = None
		
		for i in range(200):
			self.board.append([0]*200)
		self.minion = Minion()
		self.vague = Vague()

		self.enemies = []
		self.towers = []
		
		self.minion_img = 0
		self.tour_img = 0
		
		# 1 = Ennemi, 0 = Joueur
		self.current_turn = 1

		#position sur la minimap
		self.pos_x_minimap = 0
		self.pos_y_minimap = 0
		self.running = True
		
		# Une clock
		self.clock = pygame.time.Clock()
		
		# Un pygame.screen
		self.screen = 0
		
		# On place la cam au centre de la map
		w, h = pygame.display.get_surface().get_size()
		common.scale_factor = w*1.6/100
		

		self.mapdata = Map((49,16), 32, (100,100))
		self.x_off = -49*common.scale_factor+ w/2
		self.y_off = -24*common.scale_factor + h/2
			
		self.map = load_pygame(os.path.join(dossier,"../Map/Map/Map.tmx"))



		# OR
		self.gold = 10
		self.gold_income = 100
		self.gold_squelette = 7
		self.gold_gobelin = 5		
		
		# UI
		
		self.uimanager = pgu.UIManager((w, h), os.path.join(dossier, "theme.json"))
		self.gold_rect = pygame.Rect((0, 0), (80, 30))
		self.gold_rect.topleft = (30, 10)
		self.goldcounter = UITextBox(relative_rect=self.gold_rect, html_text=str(self.gold))
		
		"""
	
		self.test_rect = pygame.Rect((0, 0), (80, 30))
		self.test_rect.topleft = (230, 10)
		self.testcounter = UITextBox(relative_rect=self.test_rect, html_text=(str(self.mask_wear)))
		"""
	
		self.spawn_stack = []
		self.minions = []
		self.tours = []
		self.fleches = []
		self.init_chemins()

		tour = Tour()
		tour.center_tile = (35,55)
		tour.spawn(self.board)
		
		self.tours.append(tour)
		# Animations
		
		self.animations = self.load_animations()
		self.minion.animations = self.animations
		
	def load_animations(self):
		animations = {}
		# Animations des ennemis
		for i in os.listdir(os.path.join(dossier, "../Graphismes/Ennemis")):
			# Différents types d'ennemis
			fichier = os.path.join(dossier, "../Graphismes/Ennemis", i)
			if os.path.isdir(fichier):
				animations[i] = {}
			# Différentes directions
			for x in os.listdir(fichier):
				direction = os.path.join(fichier, x)
				if os.path.isdir(direction):
					animations[i][x] = []
					# Différentes frames
					d = os.listdir(direction)
					for f in d:
						frame = os.path.join(direction, f)
						if os.path.isfile(frame):
							# On créé une image pygame et on la scale
							image = pygame.image.load(frame)
							image = pygame.transform.scale(image, (80,80))
							animations[i][x] += [image]*(30//(len(d)))
							

		self.tour_img = pygame.image.load(os.path.join(dossier, "../Graphismes/Tours/Archers/0.png"))

		self.tour_img = pygame.transform.scale(self.tour_img, (3*common.scale_factor, 3*common.scale_factor))
		self.arrow_img = pygame.image.load(os.path.join(dossier, "../Graphismes/Tours/Archers/fleche.png"))
		self.arrow_img = pygame.transform.scale(self.arrow_img, (24,6))
		self.hammer_img =  pygame.image.load(os.path.join(dossier, "../Graphismes/hammer.png"))

		return animations
	def update_all_mvmt(self):
		for i in self.minions:
			i.mouvement_board()
		
									
	def init_chemins(self):
		# Initialise les graphes des chemins
		self.graphe_chemin_1 = Graph_node(cos=(27,87))
		
		ch1 = self.graphe_chemin_1.ajout_sortie(Graph_node(cos=(27,58)))
		self.graphe_chemin_2 = Graph_node(cos=(39,61))
		
		ch1 = ch1.ajout_sortie(Graph_node(cos=(39,57)))
		
		ch_gauche_1 = ch1.ajout_sortie(Graph_node(cos=(38,46)), 1)
		ch_millieu_1 = ch1.ajout_sortie(Graph_node(cos=(49,57)), 0.25)
		
		self.graphe_chemin_2.ajout_sortie(ch1)
		
		# Chemin de gauche
		nv = ch_gauche_1.ajout_sortie(Graph_node(cos=(23,46)),0.75)
		nv = nv.ajout_sortie(Graph_node(cos=(23,18)))
		nv = nv.ajout_sortie(Graph_node(cos=(50,18)))
		millieu_3 = nv.ajout_sortie(Graph_node(cos=(50,10)))
		
		# Chemin du millieu
		millieu_2 = ch_millieu_1.ajout_sortie(Graph_node(cos=(50,46)), 0.25)
		millieu_2.ajout_sortie(millieu_3)
		ch_gauche_1.ajout_sortie(millieu_2, 0.25)
		
		# Chemin sud-centre
		self.graphe_chemin_3 = Graph_node(cos=(87,73))
		ch3 = self.graphe_chemin_3.ajout_sortie(Graph_node(cos=(39,73)))
		ch3 = ch3.ajout_sortie(Graph_node(cos=(39, 58)))
		
		# Chemin de droite
		ch4 = ch3.ajout_sortie(Graph_node(cos=(49,58)))
		ch4 = ch4.ajout_sortie(Graph_node(cos=(72,58)))
		ch4 = ch4.ajout_sortie(Graph_node(cos=(72,20)))
		ch4.ajout_sortie(nv)
		

		
	def attaques_tours(self):
		for t in self.tours:
			for m in t.targetable_minions(self.minions):
				fleche = Fleche(m, t.cos_pixel, self.arrow_img, self.screen)
				self.fleches.append(fleche)
				m.hp -= t.damage
				print(m.hp)
				if not m.check_hp():
					self.gold += 7
					self.minions.remove(m)

	# Mettre à jour les compteurs (gold)
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
		# On créé une surface vierge et une surface avec les tiles ou on peut placer des tours en vert	
		surface = pygame.Surface((self.mapdata.tilewidth*self.mapdata.tiled_map_size[0],self.mapdata.tilewidth*self.mapdata.tiled_map_size[1])).convert()
		surface_placement = pygame.Surface((self.mapdata.tilewidth*self.mapdata.tiled_map_size[0],self.mapdata.tilewidth*self.mapdata.tiled_map_size[1])).convert()
		for layer in self.map.visible_layers:

			if layer.name == "Main":
				for x, y, img in layer.tiles():
					if img:
						surface.blit(img, (x * self.map.tilewidth,
											   y * self.map.tileheight ))
						surface_placement.blit(img, (x * self.map.tilewidth,
											   y * self.map.tileheight ))										   
			elif layer.name == "placement":
				for x, y, img in layer.tiles():
					if img:
						surface_placement.blit(img, (x * self.map.tilewidth,
											   y * self.map.tileheight ))				

		
		grid_surface = pygame.Surface((self.mapdata.tilewidth*self.mapdata.tiled_map_size[0],self.mapdata.tilewidth*self.mapdata.tiled_map_size[1]), pygame.SRCALPHA, 32).convert_alpha()
		grid_surface.set_alpha(64)
		cordx = 0
		cordy = 0
		for i in range(self.mapdata.tiled_map_size[1]):
			for i in range(self.mapdata.tiled_map_size[0]):
				rect = pygame.Rect(cordx, cordy, 32, 32)
				pygame.draw.rect(grid_surface, (0,0,0),rect, 1)
				cordx += 32
			cordx = 0
			cordy += 32
			
		surface.blit(grid_surface, (0,0))
		surface_placement.blit(grid_surface, (0,0))
		
		surface = pygame.transform.smoothscale(surface, (w*1.6, w*1.6))
		surface_placement = pygame.transform.smoothscale(surface_placement, (w*1.6, w*1.6))

		self.ennemies_in_vague = self.vague.vague_dico["vague" + str(self.minion.current_vague)]
		for ennemi, spawn in self.ennemies_in_vague:
			print(spawn)
			for _ in range(spawn):
				minion = ennemi()
				minion.animations = self.animations[str(ennemi())]				
				minion.board = self.board
				minion.spawn(self.graphe_chemin_1, self.board)
				self.spawn_stack.append(minion)


		# On remplit le plateau avec les tiles sur lesquelles on pourra placer des tours.
		for layer in self.map.visible_layers:
			if layer.name == "placement":
				for x, y, gid in layer.tiles():
					
					self.board[y][x] = common.TILE_PLACEMENT
					
				
				
		self.bottom_camera_move = pygame.Rect(0,h-100, w, 100)
		self.top_camera_move = pygame.Rect(0,-50, w, 100)
		self.right_camera_move = pygame.Rect(w-25,0, 75, h)
		self.left_camera_move = pygame.Rect(-50, 0, 75, h)
						
		minions_surface = pygame.Surface((self.mapdata.tilewidth*self.mapdata.tiled_map_size[0],self.mapdata.tilewidth*self.mapdata.tiled_map_size[1]), pygame.SRCALPHA, 32).convert_alpha()
						

		# Toutes les 250ms on lance l'event move_event qui fera que la fonction self.update_all_mvmt() sera appelée.
		move_event, t, trail = pygame.USEREVENT+1, 400, []		
		
		# Event pour l'attaque des tours toutes les 900ms
		tour_event, t2, trail2 = pygame.USEREVENT+2, 900, []		
		
		# Event pour le spawn des ennemis toutes les 900ms						
		minion_spawn_roll_event, t3, trail3 = pygame.USEREVENT+3, 2000, []								
			
		# Event pour le spawn des gobelins toutes les 900ms						
		minion_spawn_roll_event, t3, trail3 = pygame.USEREVENT+3, 2000, []		
										
		# Event pour le gain d'or toutes les secondes ms
		gold_income_event, t4, trail4 = pygame.USEREVENT+4, 1000, []								

		# Event pour le spawn d'un mob de la vague actuelle
		curr_wave_spawn_event, t5, trail5 = pygame.USEREVENT+5, 300, []								

		pygame.time.set_timer(move_event, t)
		pygame.time.set_timer(tour_event, t2)
		pygame.time.set_timer(minion_spawn_roll_event, t3)
		pygame.time.set_timer(gold_income_event, t4)
		pygame.time.set_timer(curr_wave_spawn_event, t5)
		
		
		""" Les boutons """
		self.archer_btn = Tour_build_selection_bouton(w-100,100,100,100, color=(255,215,0), sprite=self.hammer_img)
		self.boutons.append(self.archer_btn)
		while self.running:
			
			dt = self.clock.tick(30)/1000	
			Keys = pygame.key.get_pressed()		
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False
					pygame.quit()
				elif event.type == move_event:
					self.update_all_mvmt()
				elif event.type == tour_event:
					self.attaques_tours()				
					
				elif event.type == minion_spawn_roll_event:
					if random.random() < 0.5:
						minion = Minion()
						minion.animations = self.animations["Squelette"]
						minion.board = self.board
						self.minions.append(minion)	
						if random.random() < 0.5:
							minion.spawn(self.graphe_chemin_1, self.board)		
						else:
							minion.spawn(self.graphe_chemin_3, self.board)		
							
				elif event.type == gold_income_event:
					self.gold += self.gold_income	
					self.update_counters()
					
					
				elif event.type == pygame.MOUSEBUTTONUP: 
					cos = pygame.mouse.get_pos()
					# On check si un bouton est cliqué
					for i in self.boutons:
						if i.rectangle.collidepoint(cos):
							i.click(self)
					
					# On transforme les coordonnées en pixel en coordonnées en tuiles.
					
					cos_tile = (pixels_to_tile(cos[0] - self.x_off), pixels_to_tile(cos[1] - self.y_off))
					if self.tower_to_place:
						tour = self.tower_to_place()
						tour.center_tile = cos_tile					
						if self.gold >= 500 and tour.check_placable(self.board):
							tour.spawn(self.board)
							
							self.tours.append(tour)
							self.gold -= 500
							self.update_counters()

						print(cos_tile)
					
				elif event.type == curr_wave_spawn_event:
					tile_difference = random.choice([-1,0])
					if len(self.spawn_stack) > 0:
						
						self.minions.append(self.spawn_stack[0])
						randomized = self.minions[-1].cos
						# On ajoute une tile de plus ou de moins de différence aléatoirement
						# Entre chaque spawn pour qu'ils n'apparaîssent pas en ligne droite
						randomized = (randomized[0] + tile_difference, randomized[1])
						self.minions[-1].cos = randomized
						self.spawn_stack.pop(0)					


			mouse_pos = pygame.mouse.get_pos()				
			if self.bottom_camera_move.collidepoint(mouse_pos):
				self.y_off -= 48 if self.y_off > -w*1.6 + h else 0
			if self.top_camera_move.collidepoint(mouse_pos):
				self.y_off += 48 if self.y_off < 0 else 0
			if self.right_camera_move.collidepoint(mouse_pos):
				self.x_off -= 48 if self.x_off > -w*1.6 else 0
			if self.left_camera_move.collidepoint(mouse_pos):
				self.x_off += 48 if self.x_off < 0 else 0
				
				


			
			self.screen.fill((0,0,0))



			if self.tower_to_place:
				self.screen.blit(surface_placement, (self.x_off,self.y_off))
			else:
				self.screen.blit(surface, (self.x_off,self.y_off))
				

			for i in self.minions:
				i.update_animation()
				self.screen.blit(i.image, (i.cos_pixel[0] + self.x_off - 40 , i.cos_pixel[1] + self.y_off))
			for i in self.tours:
				self.screen.blit(self.tour_img, (i.cos_pixel[0] + self.x_off , i.cos_pixel[1] + self.y_off))
			for i in self.fleches:
				i.update_mouvement()
				if i.check_done():
					self.fleches.remove(i)
				self.screen.blit(i.model, (i.cos[0] + self.x_off, i.cos[1] + self.y_off))
					
			w, h = pygame.display.get_surface().get_size()

			self.uimanager.update(dt)
												
			self.uimanager.draw_ui(self.screen)
			for btn in self.boutons:
				btn.render(self.screen)
				
				

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
	
	
	
	
	
