# Un genre de mélange entre un graphe et une linked list

class Graph_node():
	def __init__(self, entree=None, sorties=[], cos=None):
		"""
		@param entree: La node avant celle-ci.
		@param sorties: une liste de tuples contenant l'objet de la prochaine node et la probabilité de s'y rendre
		@param cos: les coordonnées de ce point
		"""
		
		self.cos = cos
		self.entree = entree
		self.sorties = sorties

	def ajout_sortie(node, proba=1):
		self.sorties.append((node, proba))
		node.entree = self
		return node
