#!/usr/bin/env python

import pygame
import os
from math import sqrt, dist

import pygame_gui as pgu
import itertools as it
# Pour les maps de tiled
from pytmx import load_pygame
from pygame_gui.elements import UITextBox, UIButton
from pygame_gui.core import ObjectID
from gmap import *
from graphe import *

dossier = os.path.dirname(os.path.realpath(__file__))
Game = 0
pygame.display.set_caption("Tower Défense")
scale_factor = 0


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
		
		self.cos_pixel = (self.center_tile[0]*(w*1.6/100)- 50, self.center_tile[1]*(w*1.6/100)- 50)
	def targetable_minions(self, minions):
		ret = []
		for i in minions:
			if dist(i.cos, self.center_tile) <= self.rayon_atk:
				ret.append(i)
				return ret
				
		return ret

		
class Minion():
	def __init__(self):
		self.tile = ()
		self.hp = 1000
		self.minion_type = None
		self.node = None
		
		self.cos = (0,0)
		self.cos_pixel = (0,0)
		self.board = None
				
	def check_hp(self):
		if self.hp <= 0:
			return False
		return True
		
	def spawn(self, node, board):
		self.cos = node.cos
		self.node = node.aller_prochain()
		
		board[self.cos[0]][self.cos[1]] = self
		self.update_cos_pixel()
		
	def update_cos_pixel(self):
		w, h = pygame.display.get_surface().get_size()
		
		self.cos_pixel = (self.cos[0]*(w*1.6/100) , self.cos[1]*(w*1.6/100))
	def update_chemin(self):
		if self.cos == self.node.cos:
			self.node = self.node.aller_prochain()
			
	def mouvement_board(self):
		return
		# On retire le minion de la position ou il était preccedemment
		
		self.board[self.cos[0]][self.cos[1]] = 0
		diff = (self.node.cos[0] - self.cos[0], self.node.cos[1] - self.cos[1])
		mouvement = (0,0)
		if diff[1] > 0:
			mouvement = (0,1)
		elif diff[1] < 0:
			mouvement = (0,-1)
		elif diff[0] > 0:
			mouvement = (1,0)
		elif diff[0] < 0:
			mouvement = (-1,0)
						
		nouv_cos = (self.cos[0] + mouvement[0], self.cos[1] + mouvement[1])
		self.cos = nouv_cos
		self.update_cos_pixel()
		self.update_chemin()
	def mouvement_pixel(self):
		#TODO, NE FONCTIONNE PAS!
		
		return
		w, h = pygame.display.get_surface().get_size()
		
		diff = (self.node.cos[0]*(w*1.6/100) - self.cos_pixel[0], self.node.cos[1]*(w*1.6/100) - self.cos_pixel[1])
		mouvement = (0,0)
		if diff[1] > 0:
			mouvement = (0,scale_factor)
		elif diff[1] < 0:
			mouvement = (0,scale_factor)
		elif diff[0] > 0:
			mouvement = (scale_factor,0)
		elif diff[0] < 0:
			mouvement = (scale_factor,0)
			
		
						
		nouv_cos = (self.cos_pixel[0] + mouvement[0], self.cos_pixel[1] + mouvement[1])
		print(nouv_cos)
		self.cos_pixel = nouv_cos
		
		if nouv_cos[0] % (w*0.016) == 0 or nouv_cos[1] % (w*0.016) == 0:
			self.mouvement_board()
			
		self.update_chemin()
			
class MainGame():
	def __init__(self):
 
		self.current_scale = 1
		
		self.board = []
		self.graphe_chemin_1 = None
		for i in range(200):
			self.board.append([0]*200)

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

		self.new_x_off = 0
		self.new_y_off = 0
		
		# Une clock
		self.clock = pygame.time.Clock()
		
		# Un pygame.screen
		self.screen = 0
		
		# On place la cam au centre de la map
		w, h = pygame.display.get_surface().get_size()
		scale_factor = w*1.6/100
		

		self.mapdata = Map((49,16), 32, (100,100))
		self.x_off = -49*scale_factor+ w/2
		self.y_off = -24*scale_factor + h/2
			
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

		self.minions = []
		self.tours = []
		self.init_chemins()
		minion = Minion()
		minion.board = self.board
		minion.spawn(self.graphe_chemin_1, self.board)
		tour = Tour()
		tour.center_tile = (35,55)
		tour.spawn(self.board)
		
		self.tours.append(tour)
		self.minions.append(minion)
		
	def update_all_mvmt(self):
		for i in self.minions:
			i.mouvement_board()
		
									
	def init_chemins(self):
		# Initialise les graphes des chemins
		self.graphe_chemin_1 = Graph_node(cos=(27,70))
		
		ch1 = self.graphe_chemin_1.ajout_sortie(Graph_node(cos=(26,58)))
		self.graphe_chemin_2 = Graph_node(cos=(39,61))
		
		ch1 = ch1.ajout_sortie(Graph_node(cos=(39,57)))
		
		ch_gauche_1 = ch1.ajout_sortie(Graph_node(cos=(38,46)), 1)
		ch_millieu_1 = ch1.ajout_sortie(Graph_node(cos=(49,57)), 0.25)
		
		self.graphe_chemin_2.ajout_sortie(ch1)
		
		# Chemin de gauche
		nv = ch_gauche_1.ajout_sortie(Graph_node(cos=(23,46)),0.75)
		nv = nv.ajout_sortie(Graph_node(cos=(23,18)))
		nv = nv.ajout_sortie(Graph_node(cos=(50,18)))
		millieu_3 = nv.ajout_sortie(Graph_node(cos=(49,10)))
		
		# Chemin du millieu
		millieu_2 = ch_millieu_1.ajout_sortie(Graph_node(cos=(48,46)), 0.25)
		millieu_2.ajout_sortie(millieu_3)
		ch_gauche_1.ajout_sortie(millieu_2, 0.25)
		
		

		
	def attaques_tours(self):
		for t in self.tours:
			for m in t.targetable_minions(self.minions):
				m.hp -= t.damage
				if not m.check_hp():
					self.minions.remove(m)

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
				if img:
					surface.blit(img, (x * self.map.tilewidth,
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
		surface = pygame.transform.smoothscale(surface, (w*1.6, w*1.6))
				
		
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
		
		
				
		self.bottom_camera_move = pygame.Rect(0,h-100, w, 100)
		self.top_camera_move = pygame.Rect(0,-50, w, 100)
		self.right_camera_move = pygame.Rect(w-50,0, 100, h)
		self.left_camera_move = pygame.Rect(-50, 0, 100, h)
						
		minions_surface = pygame.Surface((self.mapdata.tilewidth*self.mapdata.tiled_map_size[0],self.mapdata.tilewidth*self.mapdata.tiled_map_size[1]), pygame.SRCALPHA, 32).convert_alpha()
						
		self.minion_img = pygame.image.load(os.path.join(dossier, "../Graphismes/Ennemis/Squelette/squelettes.png"))
		self.minion_img = pygame.transform.scale(self.minion_img, (80,80))
		self.tour_img = pygame.image.load(os.path.join(dossier, "../Graphismes/Tours/Archers/0.png"))
		self.tour_img = pygame.transform.scale(self.tour_img, (120,120))
								
		# Toutes les 250ms on lance l'event move_event qui fera que la fonction self.update_all_mvmt() sera appelée.
		move_event, t, trail = pygame.USEREVENT+1, 400, []		
		tour_event, t2, trail2 = pygame.USEREVENT+2, 900, []								
		minion_spawn_roll_event, t3, trail3 = pygame.USEREVENT+3, 900, []								
								

		pygame.time.set_timer(move_event, t)
		pygame.time.set_timer(tour_event, t2)
		pygame.time.set_timer(minion_spawn_roll_event, t2)
		
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
						minion.board = self.board
						minion.spawn(self.graphe_chemin_1, self.board)		
						self.minions.append(minion)				
					
			mouse_pos = pygame.mouse.get_pos()				
			if self.bottom_camera_move.collidepoint(mouse_pos):
				self.y_off -= 48 if self.y_off > -w*1.5 + h else 0
			if self.top_camera_move.collidepoint(mouse_pos):
				self.y_off += 48 if self.y_off < 0 else 0
			if self.right_camera_move.collidepoint(mouse_pos):
				self.x_off -= 48 if self.x_off > -w else 0
			if self.left_camera_move.collidepoint(mouse_pos):
				self.x_off += 48 if self.x_off < 0 else 0
				
				


			
			self.screen.fill((0,0,0))




			self.screen.blit(surface, (self.x_off,self.y_off))

			for i in self.minions:
				self.screen.blit(self.minion_img, (i.cos_pixel[0] + self.x_off - 100/2 , i.cos_pixel[1] + self.y_off))
			for i in self.tours:
				self.screen.blit(self.tour_img, (i.cos_pixel[0] + self.x_off , i.cos_pixel[1] + self.y_off))
								
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
	
	
	
	
	
