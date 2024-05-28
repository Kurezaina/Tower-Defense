#!/usr/bin/env python

import pygame
import os
from math import sqrt, dist, floor
import operator
import datetime

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
pygame.display.set_caption("Tower Défense")

def pixels_to_tile(pixels):
	return int(pixels/common.scale_factor)


class MainGame():
	def __init__(self):
		self.deleting_tower = False
		
		self.begin_time = datetime.datetime.now()
		self.survival_time = None
		
		# Indique si une défaite a eu lieu
		self.defeat = False
		# La chance qu'un mob apparaisse à chaque roll.
		self.spawn_chance = 0.05
		
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
		
		self.running = True
		
		# Une clock
		self.clock = pygame.time.Clock()
		
		# Un pygame.screen
		self.screen = 0
		
		# GRAPHIQUE
		w, h = pygame.display.get_surface().get_size()
		common.scale_factor = w*1.6/100
		

		self.mapdata = Map((49,16), 32, (100,100))
		self.x_off = -49*common.scale_factor+ w/2
		self.y_off = -24*common.scale_factor + h/2
			
		self.map = load_pygame(os.path.join(dossier,"../Map/Map/Map.tmx"))



		# OR
		self.gold = 500
		self.gold_income = 50
		self.gold_squelette = 7
		self.gold_gobelin = 5		


		# LISTES
		self.spawn_stack = []
		self.minions = []
		self.tours = []
		self.fleches = []
		self.init_chemins()


		# Animations
		self.fireball_img = None
		self.animations = self.load_animations()
		self.minion.animations = self.animations

	# Chargement des assets du jeu dans la RAM (GRAPHIQUE)
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
		self.mage_img = pygame.image.load(os.path.join(dossier, "../Graphismes/Tours/Mage/mage.png"))

		# Les tours doivent rentrer dans 3 cases
		self.tour_img = pygame.transform.scale(self.tour_img, (3*common.scale_factor, 3*common.scale_factor))
		self.mage_img = pygame.transform.scale(self.mage_img, (3*common.scale_factor, 3*common.scale_factor))
		
		
		self.arrow_img = pygame.image.load(os.path.join(dossier, "../Graphismes/Tours/Archers/fleche.png"))
		self.arrow_img = pygame.transform.scale(self.arrow_img, (24,6))
		
		self.fireball_img = pygame.image.load(os.path.join(dossier, "../Graphismes/Tours/Mage/boule_de_feu.png"))
		self.fireball_img = pygame.transform.scale(self.fireball_img, (24,6))
		
		self.hammer_img =  pygame.image.load(os.path.join(dossier, "../Graphismes/hammer.png"))

		return animations
		
	# Gère la mise à jour du mouvement des ennemis (TRAVAIL)
	def update_all_mvmt(self):
		for i in self.minions:
			if not i.mouvement_board():
				self.running = False
				self.defeat = True
		
									
	def init_chemins(self):
		# Initialise les graphes des chemins (TRAVAIL)
		self.graphe_chemin_1 = Graph_node(cos=(25,87))
		
		ch1 = self.graphe_chemin_1.ajout_sortie(Graph_node(cos=(25,58)))
		self.graphe_chemin_2 = Graph_node(cos=(39,61)) 
		
		ch1 = ch1.ajout_sortie(Graph_node(cos=(39,58)))
		
		ch_gauche_1 = ch1.ajout_sortie(Graph_node(cos=(38,46)), 1)
		ch_millieu_1 = ch1.ajout_sortie(Graph_node(cos=(49,58)), 0.25)
		
		self.graphe_chemin_2.ajout_sortie(ch1)
		
		# Chemin de gauche
		nv = ch_gauche_1.ajout_sortie(Graph_node(cos=(23,46)),0.75)
		nv = nv.ajout_sortie(Graph_node(cos=(23,18)))
		nv = nv.ajout_sortie(Graph_node(cos=(50,19)))
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
		ch4 = ch4.ajout_sortie(Graph_node(cos=(73,21)))
		ch4.ajout_sortie(nv)
		


	# Gère les attaques des tours et les dommages contre les mobs (TRAVAIL) #
	def attaques_tours(self):
		for t in self.tours:
			for m in t.targetable_minions(self.minions):
				fleche = Fleche(m, t.cos_pixel, t.arrow_img, self.screen)
				self.fleches.append(fleche)
				t.attack(m)
				print(m.hp)
				if not m.check_hp():
					self.gold += 7
					self.minions.remove(m)
					m.kill()

	# Mettre à jour les compteurs graphiques
	def update_counters(self):
		# Couleur du compteur d'or (blanc)
		gold_colour =  (255,255,255)

		
		font = pygame.font.Font(os.path.join(common.font_dossier, "Montserrat-Regular.ttf"))
		text = font.render(str(self.gold), True, gold_colour)
		self.screen.blit(text, (20,10))
		return
		
		
		
		
		
	def loop(self):

		# Pre-Loop: Partie Graphique# 
		
		
		# On charge la map
		w, h = pygame.display.get_surface().get_size()		
		# On créé une surface vierge et une surface avec les tiles ou on peut placer des tours en vert	
		surface = pygame.Surface((self.mapdata.tilewidth*self.mapdata.tiled_map_size[0],self.mapdata.tilewidth*self.mapdata.tiled_map_size[1])).convert()
		surface_placement = pygame.Surface((self.mapdata.tilewidth*self.mapdata.tiled_map_size[0],self.mapdata.tilewidth*self.mapdata.tiled_map_size[1])).convert()
		for layer in self.map.visible_layers:

			if layer.name == "Main" or layer.name == "terre_rouge"  or layer.name == "objet":
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


				
				
		self.bottom_camera_move = pygame.Rect(0,h-100, w, 100)
		self.top_camera_move = pygame.Rect(0,-50, w, 100)
		self.right_camera_move = pygame.Rect(w-25,0, 75, h)
		self.left_camera_move = pygame.Rect(-50, 0, 75, h)
						
		minions_surface = pygame.Surface((self.mapdata.tilewidth*self.mapdata.tiled_map_size[0],self.mapdata.tilewidth*self.mapdata.tiled_map_size[1]), pygame.SRCALPHA, 32).convert_alpha()
						
						
		""" Les boutons """
		archer_btn_icon = pygame.transform.scale(self.tour_img, (100,80))
		sorcier_btn_icon = pygame.transform.scale(self.mage_img, (100,80))
		hammer_btn_icon = pygame.transform.scale(self.hammer_img, (100,100))
		
		self.archer_btn = Archer_build_selection_bouton(w-100,100,100,100, color=(0,0,0), sprite=archer_btn_icon)
		self.sorcier_btn = Sorcier_build_selection_bouton(w-100,250,100,100, color=(0,0,0), sprite=sorcier_btn_icon)
		
		self.delete_btn = Delete_tour_button(w-100,400,100,100, color=(125,0,0), sprite=hammer_btn_icon)
		
		self.boutons.append(self.delete_btn)		
		self.boutons.append(self.archer_btn)
		self.boutons.append(self.sorcier_btn)
								
		# Pre-loop: Partie Travail # 
		
		
		self.ennemies_in_vague = self.vague.vague_dico["vague" + str(self.minion.current_vague)]
		for ennemi, spawn in self.ennemies_in_vague:
			print(spawn)
			for _ in range(spawn):
				continue
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
							

		# Toutes les 300ms on lance l'event move_event qui fera que la fonction self.update_all_mvmt() sera appelée.
		move_event, t, _ = pygame.USEREVENT+1, 300, []		
		
		# Event pour l'attaque des tours toutes les 900ms
		tour_event, t2, _ = pygame.USEREVENT+2, 900, []		
		
		# Event pour le spawn des ennemis toutes les 65ms						
		minion_spawn_roll_event, t3, _ = pygame.USEREVENT+3, 65, []								
			
										
		# Event pour le gain d'or toutes les secondes ms
		gold_income_event, t4, _ = pygame.USEREVENT+4, 1000, []								

		# Event pour le spawn d'un mob de la vague actuelle
		curr_wave_spawn_event, t5, _ = pygame.USEREVENT+5, 300, []		
								
		# Event pour l'augmentation progressive de la difficulté.
		difficulte_crescendo_event, t6, _ = pygame.USEREVENT+6, 5000, []	
		
		
		pygame.time.set_timer(move_event, t)
		pygame.time.set_timer(tour_event, t2)
		pygame.time.set_timer(minion_spawn_roll_event, t3)
		pygame.time.set_timer(gold_income_event, t4)
		pygame.time.set_timer(curr_wave_spawn_event, t5)
		pygame.time.set_timer(difficulte_crescendo_event,t6)
		
		

		
		while self.running:
		
			# Partie Travail #
			
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
					if random.random() < self.spawn_chance:
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
						# On créé un objet en fonction du type de tour (polymorphisme)
						tour = self.tower_to_place(self)
						tour.center_tile = cos_tile					
						
						if self.gold >= tour.cost and tour.check_placable(self.board):
							tour.spawn(self.board)
							self.tours.append(tour)
							self.gold -= tour.cost
							self.update_counters()

						print(cos_tile)
					elif self.deleting_tower:
						tour = [i for i in self.tours if i.center_tile == cos_tile]
						tour = tour[0] if len(tour) > 0 else None
						if tour:
							tour.despawn(self.board)
							self.tours.remove(tour)
					
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
						
				elif event.type == difficulte_crescendo_event:
					self.spawn_chance += 0.005

			
			# PARTIE GRAPHIQUE #

			mouse_pos = pygame.mouse.get_pos()				
			if self.bottom_camera_move.collidepoint(mouse_pos):
				self.y_off -= 32 if self.y_off > -w*1.6 + h else 0
			if self.top_camera_move.collidepoint(mouse_pos):
				self.y_off += 32 if self.y_off < 0 else 0
			if self.right_camera_move.collidepoint(mouse_pos):
				self.x_off -= 32 if self.x_off > -25*common.scale_factor else 0
			if self.left_camera_move.collidepoint(mouse_pos):
				self.x_off += 32 if self.x_off < -32 else 0
				
				


			
			self.screen.fill((0,0,0))



			if self.tower_to_place or self.deleting_tower:
				self.screen.blit(surface_placement, (self.x_off,self.y_off))
			else:
				self.screen.blit(surface, (self.x_off,self.y_off))
				

			for i in self.minions:
					
				i.update_animation()
				self.screen.blit(i.image, (i.cos_pixel[0] + self.x_off - 40 , i.cos_pixel[1] + self.y_off))
			for i in self.tours:
				self.screen.blit(i.sprite, (i.cos_pixel[0] + self.x_off , i.cos_pixel[1] + self.y_off))
			for i in self.fleches:
				i.update_mouvement()
				if i.check_done():
					self.fleches.remove(i)
				self.screen.blit(i.model, (i.cos[0] + self.x_off, i.cos[1] + self.y_off))
					
			w, h = pygame.display.get_surface().get_size()
			for btn in self.boutons:
				btn.render(self.screen)
				
				
			self.update_counters()
			pygame.display.flip()
			
		# On calcule cb de temps le joueur a survécu
		self.survival_time = datetime.datetime.now() - self.begin_time
			
						
if __name__ == "__main__":
	pygame.init()
	pygame.font.init()
	
	common.font_dossier = os.path.join(dossier, "fonts/")
	
	screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
	pygame.display.toggle_fullscreen()
	
	running = True

	Game = MainGame()
	common.game = Game
	Game.screen = screen
	Game.loop()
	print("T'as perdu noob")
	print(f"Temps Survécu: {Game.survival_time}")
	pygame.quit()
	
	
	
	
	
	
