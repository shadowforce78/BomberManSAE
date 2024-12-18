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


class Bomb:
    def __init__(self, x, y, size, player):
        self.x = x
        self.y = y
        self.size = size
        self.player = player
        self.sprite = None
        self.explosion_turn = player.tour + 5  # La bombe explosera dans 5 tours
        print(
            f"[DEBUG] New bomb placed at ({x},{y}), will explode at turn {self.explosion_turn}"
        )

    def draw(self):
        # Efface l'ancien sprite si il existe
        if self.sprite:
            g.supprimer(self.sprite)
        # Crée le nouveau sprite
        self.sprite = g.dessinerRectangle(
            self.x * self.size, self.y * self.size, self.size, self.size, "black"
        )

    def explode(self, map_data):
        print(f"[DEBUG] Bomb exploding at ({self.x},{self.y})")
        # Passe la référence du joueur à l'explosion
        Explosion(self.x, self.y, self.size, self.player.bomb_range, map_data, self.player)

    def remove(self):
        print(f"[DEBUG] Removing bomb sprite at ({self.x},{self.y})")
        # Efface le sprite
        if self.sprite:
            g.supprimer(self.sprite)

    def update(self, map_data, current_turn):
        if current_turn >= self.explosion_turn:
            print(f"[DEBUG] Bomb exploding at turn {current_turn}")
            self.explode(map_data)
            return True
        return False


class Explosion:
    def __init__(self, x, y, size, range, map_data, player=None):
        self.x = x
        self.y = y
        self.size = size
        self.range = range
        self.map_data = map_data
        self.player = player  # Référence au joueur qui a posé la bombe
        self.sprite = None
        self.draw()
        self.damage()

    def draw(self):
        # Efface l'ancien sprite si il existe
        if self.sprite:
            g.supprimer(self.sprite)
        # Crée le nouveau sprite
        self.sprite = g.dessinerRectangle(
            self.x * self.size, self.y * self.size, self.size, self.size, "red"
        )

    def damage(self):
        # Détruit les murs et tue les joueurs à la portée de l'explosion
        # Mur, joueur et fantôme, le reste est indestructible
        for dx, dy in [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]:
            for i in range(1, self.range + 1):
                new_x = self.x + dx * i
                new_y = self.y + dy * i
                if 0 <= new_x < len(self.map_data[0]) and 0 <= new_y < len(
                    self.map_data
                ):
                    if self.map_data[new_y][new_x] == "M":
                        # Détruit le mur
                        Block.Sol(new_x, new_y, self.size)
                        break
                    elif self.map_data[new_y][new_x] == "P":
                        if self.player:  # Si on a une référence au joueur
                            self.player.take_damage(1)
                        break
                    elif self.map_data[new_y][new_x] == "F":
                        # Détruit le fantôme
                        break
                    else:
                        # Arrête l'explosion
                        break


class Player:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.lives = 3
        self.max_bombs = 1  # Maximum number of bombs player can place
        self.active_bombs = []  # List to store active bombs
        self.bomb_range = 4
        self.speed = 1
        self.tour = 0
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
            print(
                f"[DEBUG] Player moving from ({self.x},{self.y}) to ({self.x+dx},{self.y+dy})"
            )
            self.x += dx
            self.y += dy
            # Redessine le sol à l'ancienne position
            Block.Sol(self.x - dx, self.y - dy, self.size)
            # Redessine le joueur à la nouvelle position
            self.draw()
            return True
        print(f"[DEBUG] Movement blocked at ({self.x+dx},{self.y+dy})")
        return False

    def take_damage(self, amount):
        print(f"[DEBUG] Player taking {amount} damage. Lives before: {self.lives}")
        self.lives -= amount
        print(f"[DEBUG] Lives after: {self.lives}")
        if self.lives <= 0:
            print("[DEBUG] Game Over triggered")
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
        hud_text = f"Vies: {self.lives} | Bombes: {self.max_bombs - len(self.active_bombs)} | Score: {self.score} | Tour: {self.tour}"
        g.afficherTexte(hud_text, 200, 20, "white", 16)

    def update_bombs(self, map_data):
        if self.active_bombs:
            print(
                f"[DEBUG] Updating {len(self.active_bombs)} active bombs at turn {self.tour}"
            )
        bombs_to_remove = []
        for bomb in self.active_bombs:
            if bomb.update(map_data, self.tour):
                bombs_to_remove.append(bomb)
                bomb.remove()

        if bombs_to_remove:
            print(f"[DEBUG] Removing {len(bombs_to_remove)} exploded bombs")
            self.active_bombs = [
                b for b in self.active_bombs if b not in bombs_to_remove
            ]


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
    if key:  # Seulement si une touche est pressée
        print(f"[DEBUG] Key pressed: {key}")
    if key == "Left":
        if player.move(-1, 0, map_data):
            player.tour += 1
    elif key == "Right":
        if player.move(1, 0, map_data):
            player.tour += 1
    elif key == "Up":
        if player.move(0, -1, map_data):
            player.tour += 1
    elif key == "Down":
        if player.move(0, 1, map_data):
            player.tour += 1
    elif key == "space":
        if len(player.active_bombs) < player.max_bombs:
            bomb = Bomb(player.x, player.y, player.size, player)
            bomb.draw()
            player.active_bombs.append(bomb)
            player.tour += 1
    elif key == "Escape":
        break

    # Gestion des bombes
    player.update_bombs(map_data)

    # Rafraîchit l'affichage
    g.actualiser()
    g.pause(0.05)  # Petit délai pour contrôler la vitesse du jeu

# fermeture fenêtre
g.fermerFenetre()
