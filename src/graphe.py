import random

# TRAVAIL
# Un genre de mélange entre un graphe et une linked list qui modélise le chemin des ennemis

class Graph_node():
	def __init__(self, cos=None):
		"""
		@param entree: La node avant celle-ci.
		@param sorties: une liste de tuples contenant l'objet de la prochaine node et la probabilité de s'y rendre
		@param cos: les coordonnées de ce point
		"""
		
		self.cos = cos
		self.entree = None
		self.sorties = []

	def ajout_sortie(self, node, proba=1):
		"""
		@param proba: La probabilité que cette sortie soit choisie lorsqu'on quitte la node (entre 0 et 1)
		"""
		self.sorties.append((node, proba))
		return node

	# Décide de la prochaine node vers laquelle le mob se dirigera.
	def aller_prochain(self):
		
		if random.random() <= self.sorties[0][1]:
			return self.sorties[0][0]
		else:
			return self.sorties[1][0]
