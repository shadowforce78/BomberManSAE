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
        self.fuse_sprite = None  # Nouveau sprite pour la mèche
        self.explosion_turn = player.tour + 5
        print(
            f"[DEBUG] New bomb placed at ({x},{y}), will explode at turn {self.explosion_turn}"
        )
        self.draw()  # Dessine la bombe immédiatement à la création

    def draw(self):
        # Ne redessine que si les sprites n'existent pas
        if not self.sprite:
            # Position centrale de la bombe
            center_x = self.x * self.size + self.size / 2
            center_y = self.y * self.size + self.size / 2

            # Dessine le corps de la bombe (cercle noir)
            self.sprite = g.dessinerDisque(center_x, center_y, self.size / 2.5, "black")

            # Dessine la mèche de la bombe (petit rectangle blanc)
            fuse_width = self.size / 6
            fuse_height = self.size / 3
            self.fuse_sprite = g.dessinerRectangle(
                center_x - fuse_width / 2,
                center_y - fuse_height,
                fuse_width,
                fuse_height,
                "white",
            )

    def explode(self, map_data):
        print(f"[DEBUG] Bomb exploding at ({self.x},{self.y})")
        # Passe la référence du joueur à l'explosion
        Explosion(
            self.x, self.y, self.size, self.player.bomb_range, map_data, self.player
        )

    def remove(self):
        print(f"[DEBUG] Removing bomb sprite at ({self.x},{self.y})")
        # Efface les deux sprites
        if self.sprite:
            g.supprimer(self.sprite)
            self.sprite = None
        if self.fuse_sprite:
            g.supprimer(self.fuse_sprite)
            self.fuse_sprite = None

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
        self.player = player
        self.sprites = []  # Liste pour stocker les sprites d'animation
        self.animate()
        self.damage()

    def animate(self):
        # Animation en 3 étapes rapides
        colors = ["red", "orange", "yellow"]
        for color in colors:
            # Centre de l'explosion
            center_x = self.x * self.size + self.size / 2
            center_y = self.y * self.size + self.size / 2

            # Dessine le centre
            sprite = g.dessinerDisque(center_x, center_y, self.size / 3, color)
            self.sprites.append(sprite)

            # Dessine dans les 4 directions en respectant la portée effective
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                effective_range = self.get_explosion_range(dx, dy)
                for i in range(1, effective_range + 1):
                    new_x = self.x + dx * i
                    new_y = self.y + dy * i

                    if not (
                        0 <= new_x < len(self.map_data[0])
                        and 0 <= new_y < len(self.map_data)
                    ):
                        break

                    tile = self.map_data[new_y][new_x]
                    if tile in ["C", "E"]:
                        break

                    # Dessine l'animation sur chaque case affectée
                    center_x = new_x * self.size + self.size / 2
                    center_y = new_y * self.size + self.size / 2
                    sprite = g.dessinerDisque(center_x, center_y, self.size / 3, color)
                    self.sprites.append(sprite)

                    # Si on touche un mur, on arrête dans cette direction
                    if tile == "M":
                        break

            g.actualiser()
            g.pause(0.05)  # Délai court entre chaque étape

            # Efface l'étape précédente
            for sprite in self.sprites:
                g.supprimer(sprite)
            self.sprites.clear()

    def draw(self):
        pass  # Plus besoin de cette méthode

    def get_explosion_range(self, dx, dy):
        """Calcule la portée effective de l'explosion dans une direction donnée"""
        for i in range(1, self.range + 1):
            new_x = self.x + dx * i
            new_y = self.y + dy * i

            # Vérifie les limites de la carte
            if not (
                0 <= new_x < len(self.map_data[0]) and 0 <= new_y < len(self.map_data)
            ):
                return i - 1

            tile = self.map_data[new_y][new_x]
            # Arrête à tout obstacle
            if tile in ["M", "C", "E"]:
                return i

        return self.range

    def damage(self):
        # Créer une liste des cases touchées par l'explosion
        explosion_tiles = set()

        # Ajoute la case centrale
        explosion_tiles.add((self.x, self.y))
        Block.Sol(self.x, self.y, self.size)

        # Pour chaque direction
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            max_range = self.get_explosion_range(dx, dy)
            print(f"[DEBUG] Explosion range in direction ({dx},{dy}): {max_range}")

            for i in range(1, max_range + 1):
                new_x = self.x + dx * i
                new_y = self.y + dy * i

                tile = self.map_data[new_y][new_x]

                # Ajoute la case à la zone d'explosion
                explosion_tiles.add((new_x, new_y))

                if tile == "M":
                    Block.Sol(new_x, new_y, self.size)
                    self.map_data[new_y] = (
                        self.map_data[new_y][:new_x]
                        + " "
                        + self.map_data[new_y][new_x + 1 :]
                    )
                    break  # Arrête après avoir détruit le mur
                elif tile in ["C", "E"]:
                    explosion_tiles.remove((new_x, new_y))
                    break  # Arrête à l'obstacle
                else:
                    Block.Sol(new_x, new_y, self.size)

        # Vérifie si le joueur est dans la zone d'explosion
        if self.player:
            player_pos = (int(self.player.x), int(self.player.y))
            if player_pos in explosion_tiles:
                self.player.take_damage(1)
                print(f"[DEBUG] Player hit by explosion at {player_pos}")
            else:
                print(f"[DEBUG] Player at {player_pos} safe from explosion")

        print(f"[DEBUG] Explosion affected tiles: {explosion_tiles}")

        # Call the function to replace destroyed walls
        self.replace_destroyed_walls()

    def _check_tile(self, x, y):
        # Vérifie et traite la case donnée
        if self.map_data[y][x] == "M":
            Block.Sol(x, y, self.size)
            self.map_data[y] = self.map_data[y][:x] + " " + self.map_data[y][x + 1 :]
        elif self.map_data[y][x] == "P" and self.player:
            self.player.take_damage(1)
        elif self.map_data[y][x] == "F":
            Block.Sol(x, y, self.size)
            self.map_data[y] = self.map_data[y][:x] + " " + self.map_data[y][x + 1 :]

    def replace_destroyed_walls(self):
        for y in range(len(self.map_data)):
            # Convert string to list
            row = list(self.map_data[y])
            for x in range(len(row)):
                if row[x] == "M":
                    row[x] = " "
            # Join back to string
            self.map_data[y] = "".join(row)


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
            # Suppression de bomb.draw() ici car déjà appelé dans __init__
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
