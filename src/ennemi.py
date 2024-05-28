import pygame
import random
import common

class Minion():
	def __init__(self):
		"""Classe générique pour tous les ennemis"""
		self.tile = ()
		self.hp = 1000
		self.minion_type = None
		self.node = None
		
		# La tile vers laquelle l'ennemi se dirige.
		self.target = None
		
		# Un dictionnaire contenant la liste des frames de l'animation de l'ennemi pour chaque direction
		self.animations = {}
		self.direction = "Top"
		self.image = 0
		self.frame = 0
		
		self.cos = (0, 0)
		self.cos_pixel = (0, 0)
		self.board = None
		self.current_vague = 1
		

	def check_hp(self):
		""" Vérifie si l'ennemi est toujours vivant
return: True ou False"""
		
		if self.hp <= 0:
			return False
		return True

	def spawn(self, node, board):
		""" Fait apparaitre l'ennemi sur la matrice du jeu et initialise son chemin
		@param node: la node du chemin où l'ennemi va spawn
		@board: la matrice du jeu
		"""
		self.cos = node.cos
		self.node = node.aller_prochain()
		self.target = self.node.cos
		board[self.cos[1]][self.cos[0]] = self
		self.update_cos_pixel()

	def update_cos_pixel(self):
		w, h = pygame.display.get_surface().get_size()

		self.cos_pixel = (self.cos[0] * (w * 1.6 / 100), self.cos[1] * (w * 1.6 / 100))

	def update_chemin(self):
		"""Met à jour le chemin de l'ennemi
		En le faisant se diriger vers la prochaine node du graphe"""
		

		if self.cos == self.target:
			# Défaite si l'ennemi est parvenu à la dernière tile, on retourne false.
			if len(self.node.sorties) == 0:
				return False		
			self.node = self.node.aller_prochain()
			# On randomise la destination du minion pour qu'ils ne soient pas tous en ligne droite
			self.target = (self.node.cos[0] + random.randint(-1,1), self.node.cos[1] + random.randint(-1,1))
		return True
			
	def mouvement_board(self):
		""" Met a jour la position de l'ennemi sur la matrice du jeu
		En faisant un pathfinding simple vers la node vers laquelle l'ennemi se dirige.
		"""
		# On retire le minion de la position ou il était preccedemment

		self.board[self.cos[1]][self.cos[0]] = 0
		diff = (self.target[0] - self.cos[0], self.target[1] - self.cos[1])
		mouvement = (0, 0)
		prev_direction = self.direction
		
		# Mouvement vers le bas 
		if diff[1] > 0:
			mouvement = (0, 1)
			self.direction = "Bottom"
			
		# Mouvement vers le haut
		elif diff[1] < 0:
			mouvement = (0, -1)
			self.direction = "Top"
		# Mouvement droite
		elif diff[0] > 0:
			mouvement = (1, 0)
			self.direction = "Right"
		# Mouvement gauche
		elif diff[0] < 0:
			mouvement = (-1, 0)
			self.direction = "Left"
			
		if self.direction != prev_direction:
			 self.frame = 0

		nouv_cos = (self.cos[0] + mouvement[0], self.cos[1] + mouvement[1])
		self.cos = nouv_cos
		self.update_cos_pixel()
		
		return self.update_chemin()
		
	def update_animation(self):
		"""Passe à la prochaine frame de l'animation de l'ennemi"""
		if self.frame >= len(self.animations[self.direction]) - 1:
			self.frame = 0
			
		next_frame = self.animations[self.direction][self.frame]
		self.image = next_frame
		
		self.frame += 1

	def kill(self):
		"""Retire l'unité de la matrice du jeu"""
		
		self.board[self.cos[1]][self.cos[0]] = 0
		
# + rapide, moins de PV
class Gobelin(Minion):
	def __init__(self):
		super(Gobelin, self).__init__()
		self.hp = 600
	def __str__(self):
		return "Gobelin"
		
# Ennemi générique avec des stats de base
class Squelette(Minion):
	def __init__(self):
		super(Squelette, self).__init__()
	def __str__(self):
		return "Squelette"

# Vague 1 : 15 squelettes et 15 gobelins
class Vague():
	def __init__(self):
		self.vague_dico = {
			"vague1" : [(Squelette, 15), (Gobelin, 0)]

		}
