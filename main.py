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
        self.fuse_sprite = None
        self.placed_at = player.timer # Stocke le timer au moment du placement
        self.explosion_timer = self.placed_at - 5 # Explose quand le timer atteint cette valeur
        print(f"[DEBUG] New bomb placed at ({x},{y}), will explode at timer {self.explosion_timer}")
        self.draw()

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

    def update(self, map_data, current_timer):
        if current_timer <= self.explosion_timer:  # Change la condition pour exploser quand le timer atteint la valeur cible
            print(f"[DEBUG] Bomb exploding at timer {current_timer}")
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
        self.damage()  # Do damage first
        self.animate()  # Then animate the results

    def animate(self):
        colors = ["red", "orange", "yellow"]
        for color in colors:
            current_sprites = []
            # Centre de l'explosion
            center_x = self.x * self.size + self.size / 2
            center_y = self.y * self.size + self.size / 2

            sprite = g.dessinerDisque(center_x, center_y, self.size / 3, color)
            current_sprites.append(sprite)

            # Pour chaque direction
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                walls_hit = 0
                for i in range(1, self.range + 1):
                    new_x = self.x + dx * i
                    new_y = self.y + dy * i

                    if not (
                        0 <= new_x < len(self.map_data[0])
                        and 0 <= new_y < len(self.map_data)
                    ):
                        break

                    tile = self.map_data[new_y][new_x]

                    # Draw animation
                    center_x = new_x * self.size + self.size / 2
                    center_y = new_y * self.size + self.size / 2
                    sprite = g.dessinerDisque(center_x, center_y, self.size / 3, color)
                    current_sprites.append(sprite)

                    # Stop at columns and ethernet ports
                    if tile in ["C", "E"]:
                        break
                    # Count walls and stop after 4
                    elif tile == "M":
                        walls_hit += 1
                        if walls_hit >= 4:
                            break

            g.actualiser()
            g.pause(0.05)

            # Clean up current color's sprites
            for sprite in current_sprites:
                g.supprimer(sprite)

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
        explosion_tiles = set()
        destroyed_blocks = []

        # Ajoute la case centrale
        explosion_tiles.add((self.x, self.y))
        print(f"[DEBUG] Starting explosion at ({self.x}, {self.y})")

        # Pour chaque direction
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            direction_name = {
                (1, 0): "droite",
                (-1, 0): "gauche",
                (0, 1): "bas",
                (0, -1): "haut",
            }
            print(f"[DEBUG] Checking direction: {direction_name[(dx,dy)]}")
            walls_destroyed = 0  # Compteur de murs détruits dans cette direction

            for i in range(1, self.range + 1):
                new_x = self.x + dx * i
                new_y = self.y + dy * i

                if not (
                    0 <= new_x < len(self.map_data[0])
                    and 0 <= new_y < len(self.map_data)
                ):
                    print(f"[DEBUG] Hit map boundary at ({new_x}, {new_y})")
                    break

                tile = self.map_data[new_y][new_x]
                explosion_tiles.add((new_x, new_y))
                print(f"[DEBUG] Checking tile at ({new_x}, {new_y}): '{tile}'")

                if tile == "M":
                    walls_destroyed += 1
                    print(
                        f"[DEBUG] Destroying wall at ({new_x}, {new_y}). Wall count: {walls_destroyed}"
                    )
                    destroyed_blocks.append((new_x, new_y))
                    Block.Sol(new_x, new_y, self.size)
                    row = list(self.map_data[new_y])
                    row[new_x] = " "
                    self.map_data[new_y] = "".join(row)
                    if self.player:  # Add 1 to score for each wall destroyed
                        self.player.score += 1
                    if walls_destroyed >= 4:  # Stop after destroying 4 walls
                        break
                elif tile in ["C", "E"]:
                    print(f"[DEBUG] Hit indestructible obstacle at ({new_x}, {new_y})")
                    explosion_tiles.remove((new_x, new_y))
                    break
                else:
                    print(
                        f"[DEBUG] Explosion continues through empty space at ({new_x}, {new_y})"
                    )
                    Block.Sol(new_x, new_y, self.size)

        print(f"[DEBUG] Total blocks destroyed: {len(destroyed_blocks)}")
        print(f"[DEBUG] Destroyed blocks positions: {destroyed_blocks}")

        # Check player damage
        if self.player:
            player_pos = (int(self.player.x), int(self.player.y))
            if player_pos in explosion_tiles:
                print(f"[DEBUG] Player hit at position {player_pos}")
                self.player.take_damage(1)
                self.player.draw()  # Redraw the player to ensure it doesn't disappear

    def replace_destroyed_walls(self):
        # Cette méthode n'est plus nécessaire car les murs sont correctement gérés dans damage()
        pass


class Player:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.lives = 3
        self.max_bombs = 1  # Maximum de bombes actives à la fois
        self.active_bombs = []  # Pour stocker les bombes
        self.bomb_range = 4  # Distance des explosions par défaut
        self.lvl = 0
        self.speed = 1
        self.timer = 0  # Sera initialisé avec la valeur du fichier
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
        # Texte du HUD
        hud_text = f"Vies:{self.lives:3d} | Bombes:{self.max_bombs - len(self.active_bombs):2d} | Timer:{self.timer:4d} | Score:{self.score:5d} | Niveau:{self.lvl:2d}"
        # Dessine le fond du HUD
        g.dessinerRectangle(0, 0, 800, 40, "black")
        # Affiche le texte du HUD
        g.afficherTexte(hud_text, 400, 20, "white", 16)

    def update_bombs(self, map_data):
        if self.active_bombs:
            print(
                f"[DEBUG] Updating {len(self.active_bombs)} active bombs at timer {self.timer}"
            )
        bombs_to_remove = []
        for bomb in self.active_bombs:
            if bomb.update(map_data, self.timer):  # Changed from tour to timer
                bombs_to_remove.append(bomb)
                bomb.remove()

        if bombs_to_remove:
            print(f"[DEBUG] Removing {len(bombs_to_remove)} exploded bombs")
            self.active_bombs = [
                b for b in self.active_bombs if b not in bombs_to_remove
            ]

    def update_timer(self):
        self.timer -= 1
        if self.timer < 0:
            print("[DEBUG] Time's up!")
            g.afficherTexte("Time's Up!", 200, 200, "red", 32)
            g.actualiser()
            g.attendreClic()
            g.fermerFenetre()


def readmap1():
    players = []
    with open("map0.txt", "r") as file:
        map1 = file.readlines()
        
    # Lecture des paramètres des deux premières lignes
    time = int(map1[0].split()[1])
    timerfantome = int(map1[1].split()[1])
    print(f"[DEBUG] Time: {time}, Timer Fantome: {timerfantome}")

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
                player.timer = time  # Initialisation du timer avec la valeur lue
                players.append(player)
                player.draw()
    return players, map1[3:], time, timerfantome

# Récupère les joueurs et la carte
players, map_data, time, timerfantome = readmap1()
player = players[0]  # Le premier joueur

# Boucle principale du jeu
while True:
    # Affiche le nouveau HUD
    player.draw_hud()

    # Récupère la touche pressée
    key = g.recupererTouche()

    # Gestion des mouvements
    if key:  # Seulement si une touche est pressée
        print(f"[DEBUG] Key pressed: {key}")
    if key == "Left":
        if player.move(-1, 0, map_data):
            player.update_timer()
    elif key == "Right":
        if player.move(1, 0, map_data):
            player.update_timer()
    elif key == "Up":
        if player.move(0, -1, map_data):
            player.update_timer()
    elif key == "Down":
        if player.move(0, 1, map_data):
            player.update_timer()
    elif key == "space":
        if len(player.active_bombs) < player.max_bombs:
            bomb = Bomb(player.x, player.y, player.size, player)
            player.active_bombs.append(bomb)
            player.update_timer()
    elif key == "Escape":
        break

    # Gestion des bombes
    player.update_bombs(map_data)

    # Rafraîchit l'affichage
    g.actualiser()
    g.pause(0.05)  # Petit délai pour contrôler la vitesse du jeu

# fermeture fenêtre
g.fermerFenetre()
