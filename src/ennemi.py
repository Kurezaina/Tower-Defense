import pygame
import common

class Minion():
    def __init__(self):
        self.tile = ()
        self.hp = 1000
        self.minion_type = None
        self.node = None

        self.cos = (0, 0)
        self.cos_pixel = (0, 0)
        self.board = None
        self.current_vague = 1

    def check_hp(self):
        if self.hp <= 0:
            return False
        return True

    def spawn(self, node, board):
        self.cos = node.cos
        self.node = node.aller_prochain()

        board[self.cos[1]][self.cos[0]] = self
        self.update_cos_pixel()

    def update_cos_pixel(self):
        w, h = pygame.display.get_surface().get_size()

        self.cos_pixel = (self.cos[0] * (w * 1.6 / 100), self.cos[1] * (w * 1.6 / 100))

    def update_chemin(self):
        if self.cos == self.node.cos:
            self.node = self.node.aller_prochain()

    def mouvement_board(self):
        # On retire le minion de la position ou il était preccedemment

        self.board[self.cos[1]][self.cos[0]] = 0
        diff = (self.node.cos[0] - self.cos[0], self.node.cos[1] - self.cos[1])
        mouvement = (0, 0)
        if diff[1] > 0:
            mouvement = (0, 1)
        elif diff[1] < 0:
            mouvement = (0, -1)
        elif diff[0] > 0:
            mouvement = (1, 0)
        elif diff[0] < 0:
            mouvement = (-1, 0)

        nouv_cos = (self.cos[0] + mouvement[0], self.cos[1] + mouvement[1])
        self.cos = nouv_cos
        self.update_cos_pixel()
        self.update_chemin()

    def mouvement_pixel(self):
        # TODO, NE FONCTIONNE PAS!

        return
        w, h = pygame.display.get_surface().get_size()

        diff = (
        self.node.cos[0] * (w * 1.6 / 100) - self.cos_pixel[0], self.node.cos[1] * (w * 1.6 / 100) - self.cos_pixel[1])
        mouvement = (0, 0)
        if diff[1] > 0:
            mouvement = (0, scale_factor)
        elif diff[1] < 0:
            mouvement = (0, scale_factor)
        elif diff[0] > 0:
            mouvement = (scale_factor, 0)
        elif diff[0] < 0:
            mouvement = (scale_factor, 0)

        nouv_cos = (self.cos_pixel[0] + mouvement[0], self.cos_pixel[1] + mouvement[1])
        print(nouv_cos)
        self.cos_pixel = nouv_cos

        if nouv_cos[0] % (w * 0.016) == 0 or nouv_cos[1] % (w * 0.016) == 0:
            self.mouvement_board()

        self.update_chemin()


# Vague 1 : 15 squelettes et 15 gobelins

class Vague():
    def __init__(self):
        self.vague_dico = {
            "vague1" : [("squelettes", 15), ("gobelins", 15)]

        }

