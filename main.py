# coding: utf-8
from tkiteasy import *
import random
import math

# ouverture de fenêtre
L, H = 800, 800
g = ouvrirFenetre(L, H)

# un mur (M)
# une colonne (C)
# une prise ethernet (E)
# Pour les cases vides
# le bomberman (P)
# un fantôme (F)
# un upgrade (U)
# une bombe (B)
# une explosion (X)


class Block:
    def __init__(self, x, y, c):
        self.x = x
        self.y = y
        self.c = c

    def Colonne(x, y, c):
        g.dessinerRectangle(x * c, y * c, c, c, "DarkSlateGray")
        g.dessinerLigne(x * c, y * c, x * c, y * c + c, "black")
        g.dessinerLigne(x * c, y * c, x * c + c, y * c, "black")
        g.dessinerLigne(x * c, y * c + c, x * c + c, y * c + c, "black")
        g.dessinerLigne(x * c + c, y * c, x * c + c, y * c + c, "black")
        g.dessinerLigne(x * c, y * c + c, x * c + c, y * c, "black")
        g.dessinerLigne(x * c, y * c, x * c + c, y * c + c, "black")

    def Mur(x, y, c):
        g.dessinerRectangle(x * c, y * c, c, c, "firebrick")
        g.dessinerLigne(x * c, y * c, x * c, y * c + c, "darkred")
        g.dessinerLigne(x * c, y * c, x * c + c, y * c, "darkred")
        g.dessinerLigne(x * c, y * c + c, x * c + c, y * c + c, "darkred")
        g.dessinerLigne(x * c + c, y * c, x * c + c, y * c + c, "darkred")
        g.dessinerLigne(
            x * c + (c // 2),
            y * c + (c // 3.5),
            x * c + (c // 2),
            y * c + (c // 2),
            "darkred",
        )
        g.dessinerLigne(
            x * c + (c // 2), y * c + (c // 1.3), x * c + (c // 2), y * c + c, "darkred"
        )
        g.dessinerLigne(
            x * c + (c // 3.5), y * c, x * c + (c // 3.5), y * c + (c // 3.5), "darkred"
        )
        g.dessinerLigne(
            x * c + (c // 1.3), y * c, x * c + (c // 1.3), y * c + (c // 3.5), "darkred"
        )
        g.dessinerLigne(
            x * c + (c // 3.5),
            y * c + (c // 2),
            x * c + (c // 3.5),
            y * c + (c // 1.3),
            "darkred",
        )
        g.dessinerLigne(
            x * c + (c // 1.3),
            y * c + (c // 2),
            x * c + (c // 1.3),
            y * c + (c // 1.3),
            "darkred",
        )
        g.dessinerLigne(x * c, y * c + (c // 2), x * c + c, y * c + (c // 2), "darkred")
        g.dessinerLigne(
            x * c, y * c + (c // 3.5), x * c + c, y * c + (c // 3.5), "darkred"
        )
        g.dessinerLigne(
            x * c, y * c + (c // 1.3), x * c + c, y * c + (c // 1.3), "darkred"
        )  # in process of renovation

    def Sol(x, y, c):
        g.dessinerRectangle(x * c, y * c, c, c, "tan")
        g.dessinerLigne(x * c, y * c, x * c + c, y * c, "brown")
        g.dessinerLigne(x * c, y * c + (c // 2), x * c + c, y * c + (c // 2), "brown")
        g.dessinerLigne(
            x * c, y * c + (c // 1.3), x * c + c, y * c + (c // 1.3), "brown"
        )
        g.dessinerLigne(
            x * c, y * c + (c // 3.5), x * c + c, y * c + (c // 3.5), "brown"
        )

    def Ethernet(x, y, c):
        g.dessinerRectangle(x * c, y * c, c, c, "BlanchedAlmond")
        g.dessinerLigne(
            x * c + (c // 3.5),
            y * c + (c // 3.5),
            x * c + (c // 3.5),
            y * c + (c // 1.3),
            "black",
        )
        g.dessinerLigne(
            x * c + (c // 1.3),
            y * c + (c // 3.5),
            x * c + (c // 1.3),
            y * c + (c // 1.3),
            "black",
        )
        g.dessinerLigne(
            x * c + (c // 3.5),
            y * c + (c // 3.5),
            x * c + (c // 1.3),
            y * c + (c // 3.5),
            "black",
        )
        g.dessinerLigne(
            x * c + (c // 3.5),
            y * c + (c // 1.3),
            x * c + (c // 1.3),
            y * c + (c // 1.3),
            "black",
        )


class Player:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.lives = 3
        self.bombs = 1
        self.bomb_range = 4
        self.speed = 1
        self.sprite = None
        self.score = 0

    def draw(self):
        # Efface l'ancien sprite si il existe
        if self.sprite:
            g.supprimer(self.sprite)
        # Crée le nouveau sprite
        self.sprite = g.dessinerRectangle(
            self.x * self.size, self.y * self.size, self.size, self.size, "Yellow"
        )

    def move(self, dx, dy, map_data):
        if self.can_move(dx, dy, map_data):
            self.x += dx
            self.y += dy
            # Redessine le sol à l'ancienne position
            Block.Sol(self.x - dx, self.y - dy, self.size)
            # Redessine le joueur à la nouvelle position
            self.draw()
            return True
        return False

    def take_damage(self, amount):
        self.lives -= amount
        if self.lives <= 0:
            # Game over
            g.afficherTexte("Game Over", 200, 200, "red", 32)
            g.actualiser()
            g.attendreClic()
            g.fermerFenetre()

    def can_move(self, dx, dy, map_data):
        # Calcule la nouvelle position
        new_x = self.x + dx
        new_y = self.y + dy

        # Vérifie si la nouvelle position est dans les limites et n'est pas un mur/colonne
        if 0 <= new_x < len(map_data[0]) and 0 <= new_y < len(map_data):
            return map_data[int(new_y)][int(new_x)] not in ["M", "C", "E"]
        return False

    def draw_hud(self):
        # Affiche l'ATH en haut à gauche avec des caractères ASCII
        hud_text = f"Vies: {self.lives} | Bombes: {self.bombs} | Score: {self.score}"
        g.afficherTexte(hud_text, 200, 20, "white", 16)  # x changé de 120 à 200


def readmap1():
    players = []
    with open("map0.txt", "r") as file:
        map1 = file.readlines()
    for col in range(0, len(map1) - 3):
        mp = map1[col + 3].strip()
        print(repr(mp))
        BI = len(mp)
        for lig in range(0, len(mp)):
            if mp[lig] == "C":
                Block.Colonne(lig, col, L // BI)
            elif mp[lig] == "M":
                Block.Mur(lig, col, L // BI)
            elif mp[lig] == "E":
                Block.Ethernet(lig, col, L // BI)
            elif mp[lig] == " ":
                Block.Sol(lig, col, L // BI)
            elif mp[lig] == "P":
                player = Player(lig, col, L // BI)
                players.append(player)
                player.draw()
    return players, map1[3:]  # Retourne aussi les données de la carte


# Récupère les joueurs et la carte
players, map_data = readmap1()
player = players[0]  # Le premier joueur

# Boucle principale du jeu
while True:
    # Efface l'ancien HUD avec un rectangle noir (fond)
    g.dessinerRectangle(
        0, 0, 400, 40, "black"
    )  # largeur changée de 300 à 400 pour s'assurer que tout le texte est visible
    # Affiche le nouveau HUD
    player.draw_hud()

    # Récupère la touche pressée
    key = g.recupererTouche()

    # Gestion des mouvements
    if key == "Left":
        player.move(-1, 0, map_data)
    elif key == "Right":
        player.move(1, 0, map_data)
    elif key == "Up":
        player.move(0, -1, map_data)
    elif key == "Down":
        player.move(0, 1, map_data)
    elif key == "Escape":
        break

    # Rafraîchit l'affichage
    g.actualiser()
    g.pause(0.05)  # Petit délai pour contrôler la vitesse du jeu

# fermeture fenêtre
g.fermerFenetre()
