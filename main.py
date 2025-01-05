# coding: utf-8
from tkiteasy import *
import random
import math

# Configuration globale
DEBUG_MODE = False  # Variable pour activer/désactiver les prints de debug

def debug_print(*args, **kwargs):
    if DEBUG_MODE:
        print(*args, **kwargs)

# ouverture de fenêtre
L, H = 800, 800
g = ouvrirFenetre(L, H)
fantomes = []  # Liste globale des fantômes
current_ghost_timer = 0  # Timer pour le spawn des fantômes

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
        )

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
        self.placed_at = player.timer  # Stocke le timer au moment du placement
        self.explosion_timer = (
            self.placed_at - 5
        )  # Explose quand le timer atteint cette valeur
        debug_print(f"New bomb placed at ({x},{y}), will explode at timer {self.explosion_timer}")
        self.draw()

    def draw(self):
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
        debug_print(f"Bomb exploding at ({self.x},{self.y})")
        # Passe la référence du joueur à l'explosion
        Explosion(
            self.x, self.y, self.size, self.player.bomb_range, map_data, self.player
        )

    def remove(self):
        debug_print(f"Removing bomb sprite at ({self.x},{self.y})")
        # Efface les deux sprites
        if self.sprite:
            g.supprimer(self.sprite)
            self.sprite = None
        if self.fuse_sprite:
            g.supprimer(self.fuse_sprite)
            self.fuse_sprite = None

    def update(self, map_data, current_timer):
        if current_timer <= self.explosion_timer:
            debug_print(f"Bomb exploding at timer {current_timer}")
            self.remove()  # D'abord on supprime les sprites de la bombe
            self.explode(map_data)  # Ensuite on crée l'explosion
            return True
        else:
            # On redessine la bombe uniquement si elle n'a pas encore explosé
            self.draw()
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
        self.ghost_tiles = (
            set()
        )  # Ajout d'un set pour suivre les positions des fantômes touchés
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
        ghosts_to_destroy = []  # Liste des fantômes à détruire

        # Ajoute la case centrale
        explosion_tiles.add((self.x, self.y))
        debug_print(f"Starting explosion at ({self.x}, {self.y})")

        # Pour chaque direction
        for dx, dy in [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]:
            direction_name = {
                (0, 0): "centre",
                (1, 0): "droite",
                (-1, 0): "gauche",
                (0, 1): "bas",
                (0, -1): "haut",
            }
            debug_print(f"Checking direction: {direction_name[(dx,dy)]}")
            walls_destroyed = 0  # Compteur de murs détruits dans cette direction

            for i in range(1, self.range + 1):
                new_x = self.x + dx * i
                new_y = self.y + dy * i

                if not (
                    0 <= new_x < len(self.map_data[0])
                    and 0 <= new_y < len(self.map_data)
                ):
                    debug_print(f"Hit map boundary at ({new_x}, {new_y})")
                    break

                # Vérifie les fantômes à cette position
                for ghost in list(
                    fantomes
                ):  # Utilise une copie de la liste pour éviter les problèmes de modification pendant l'itération
                    if (
                        ghost.visible
                        and int(ghost.x) == new_x
                        and int(ghost.y) == new_y
                    ):
                        debug_print(f"Ghost #{ghost.id} caught in explosion at ({new_x}, {new_y})")
                        ghosts_to_destroy.append(ghost)

                tile = self.map_data[new_y][new_x]
                explosion_tiles.add((new_x, new_y))
                debug_print(f"Checking tile at ({new_x}, {new_y}): '{tile}'")

                if tile == "M":
                    walls_destroyed += 1
                    debug_print(f"Destroying wall at ({new_x}, {new_y}). Wall count: {walls_destroyed}")
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
                    debug_print(f"Hit indestructible obstacle at ({new_x}, {new_y})")
                    explosion_tiles.remove((new_x, new_y))
                    break
                else:
                    debug_print(f"Explosion continues through empty space at ({new_x}, {new_y})")
                    Block.Sol(new_x, new_y, self.size)

        # Détruit tous les fantômes touchés
        for ghost in ghosts_to_destroy:
            ghost.destroy()
            if self.player:  # Ajoute des points pour chaque fantôme détruit
                self.player.score += 5  # Plus de points que pour un mur
                debug_print(f"Player scored 5 points for destroying ghost #{ghost.id}")

        debug_print(f"Total blocks destroyed: {len(destroyed_blocks)}")
        debug_print(f"Destroyed blocks positions: {destroyed_blocks}")

        # Check player damage
        if self.player:
            player_pos = (int(self.player.x), int(self.player.y))
            if player_pos in explosion_tiles:
                debug_print(f"Player hit at position {player_pos}")
                self.player.take_damage(1)
                self.player.draw()  # Redraw the player to ensure it doesn't disappear


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
        self.last_collision_check = (
            0  # Nouveau: pour suivre le dernier check de collision
        )

    def draw(self):
        # Efface l'ancien sprite s'il existe
        if self.sprite:
            g.supprimer(self.sprite)

        center_x = self.x * self.size + self.size / 2
        center_y = self.y * self.size + self.size / 2

        # Corps du joueur
        self.sprite = g.dessinerDisque(center_x, center_y, self.size / 2, "Yellow")

        # Yeux du joueur
        eye_radius = self.size / 10
        eye_offset = self.size / 6
        for dx in (-eye_offset, eye_offset):
            g.dessinerDisque(center_x + dx, center_y - eye_offset, eye_radius, "Black")

        # Bouche du joueur
        mouth_width = self.size / 3
        mouth_height = self.size / 10
        mouth_y = center_y + eye_offset
        g.dessinerLigne(
            center_x - mouth_width / 2,
            mouth_y,
            center_x,
            mouth_y + mouth_height,
            "Black",
        )
        g.dessinerLigne(
            center_x,
            mouth_y + mouth_height,
            center_x + mouth_width / 2,
            mouth_y,
            "Black",
        )

    def move(self, dx, dy, map_data):
        if self.can_move(dx, dy, map_data):
            debug_print(f"Player moving from ({self.x},{self.y}) to ({self.x+dx},{self.y+dy})")
            self.x += dx
            self.y += dy
            # Redessine le sol à l'ancienne position
            Block.Sol(self.x - dx, self.y - dy, self.size)
            # Redessine le joueur à la nouvelle position
            self.draw()
            return True
        debug_print(f"Movement blocked at ({self.x+dx},{self.y+dy})")
        return False

    def take_damage(self, amount):
        debug_print(f"Player taking {amount} damage. Lives before: {self.lives}")
        self.lives -= amount
        debug_print(f"Lives after: {self.lives}")
        if self.lives < 1:
            debug_print("Game Over triggered")
            g.afficherTexte("Game Over", 200, 200, "red", 32)
            g.actualiser()
            g.attendreClic()
            g.fermerFenetre()

    def can_move(self, dx, dy, map_data):
        new_x = self.x + dx
        new_y = self.y + dy

        # Vérifie si la nouvelle position est dans les limites et n'est pas un obstacle
        if 0 <= new_x < len(map_data[0]) and 0 <= new_y < len(map_data):
            # Vérifie s'il y a un fantôme à la nouvelle position
            for fantome in fantomes:
                if int(fantome.x) == int(new_x) and int(fantome.y) == int(new_y):
                    return False
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
            debug_print(f"Updating {len(self.active_bombs)} active bombs at timer {self.timer}")
        bombs_to_remove = []
        for bomb in self.active_bombs:
            if bomb.update(map_data, self.timer):  # Changed from tour to timer
                bombs_to_remove.append(bomb)
                bomb.remove()

        if bombs_to_remove:
            debug_print(f"Removing {len(bombs_to_remove)} exploded bombs")
            self.active_bombs = [
                b for b in self.active_bombs if b not in bombs_to_remove
            ]

    def update_timer(self):
        self.timer -= 1
        if self.timer < 0:
            debug_print("Time's up!")
            g.afficherTexte("Time's Up!", 200, 200, "red", 32)
            g.actualiser()
            g.attendreClic()
            g.fermerFenetre()

    def check_ghost_collision(self):
        """Vérifie si un fantôme est adjacent au joueur et inflige des dégâts si c'est le cas"""
        # Ne vérifie qu'une fois par tour
        if self.last_collision_check == self.timer:
            return False

        self.last_collision_check = self.timer
        for fantome in fantomes:
            if (
                fantome.visible
                and abs(self.x - fantome.x) <= 1
                and abs(self.y - fantome.y) <= 1
            ):
                debug_print(f"Player adjacent to ghost #{fantome.id}")
                self.take_damage(1)
                return True
        return False


class Fantome:

    # Les fantômes se déplacent une case par tour sur des cases non bloquantes.
    # Si un Bomber est adjacent, le fantôme ne bouge pas (il attend pour attaquer).
    # Les déplacements respectent ces règles :
    # Aucune case voisine disponible : Le fantôme reste immobile.
    # Une seule case disponible : Le fantôme s'y déplace.
    # Plusieurs cases disponibles : Une case est choisie aléatoirement, en excluant la case occupée au tour précédent (évite les retours inutiles).

    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.sprite = None
        self.last_pos = None  # Pour éviter de revenir en arrière
        self.visible = False  # État de visibilité du fantôme
        self.next_apparition = 0  # Prochain timer d'apparition
        self.has_moved = (
            False  # Nouvel attribut pour suivre si le fantôme a bougé ce tour
        )
        self.id = len(fantomes)  # Ajouter un identifiant unique
        self.blocked_turns = 0  # Compteur de tours bloqués
        self.just_attacked = False  # New attribute to track attack state
        debug_print(f"Created ghost #{self.id} at position ({x}, {y})")

    def draw(self):
        if self.sprite:
            g.supprimer(self.sprite)
        if self.visible:  # Dessine seulement si visible
            self.sprite = g.dessinerDisque(
                self.x * self.size + self.size / 2,
                self.y * self.size + self.size / 2,
                self.size / 2,
                "purple",
            )
            debug_print(f"Ghost #{self.id} drawn at ({self.x}, {self.y})")

    def hide(self):
        if self.sprite:
            g.supprimer(self.sprite)
            self.sprite = None
            debug_print(f"Ghost #{self.id} hidden")
        self.visible = False

    def show(self):
        self.visible = True
        debug_print(f"Ghost #{self.id} shown")
        self.draw()

    def get_available_moves(self, map_data):
        moves = []
        debug_print(f"Ghost #{self.id} checking available moves from ({self.x}, {self.y})")
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_x = int(self.x + dx)
            new_y = int(self.y + dy)

            # Vérifie si la nouvelle position est valide
            if (
                0 <= new_x < len(map_data[0])
                and 0 <= new_y < len(map_data)
                and map_data[new_y][new_x] not in ["M", "C", "E"]
                and (new_x, new_y) != self.last_pos
            ):

                # Vérifie si la case est occupée par un autre fantôme visible
                occupied = False
                for f in fantomes:
                    if (
                        f != self
                        and f.visible
                        and int(f.x) == new_x
                        and int(f.y) == new_y
                    ):
                        debug_print(f"Ghost #{self.id} found position ({new_x}, {new_y}) occupied by Ghost #{f.id}")
                        occupied = True
                        break

                if not occupied:
                    moves.append((dx, dy))
                    debug_print(f"Ghost #{self.id} found valid move to ({new_x}, {new_y})")

        debug_print(f"Ghost #{self.id} has {len(moves)} possible moves")
        return moves

    def move(self, map_data):
        if (
            not self.visible or self.has_moved
        ):  # Ne bouge pas si invisible ou déjà bougé
            if not self.visible:
                debug_print(f"Ghost #{self.id} is invisible, skipping move")
            if self.has_moved:
                debug_print(f"Ghost #{self.id} has already moved this turn")
            return

        # Si le fantôme vient d'attaquer, il ne peut pas bouger ce tour
        if self.just_attacked:
            debug_print(f"Ghost #{self.id} cooling down after attack")
            self.just_attacked = False  # Reset pour le prochain tour
            return

        # Vérifie si un joueur est adjacent (horizontalement ou verticalement)
        for player in players:
            if (abs(self.x - player.x) == 1 and self.y == player.y) or (
                abs(self.y - player.y) == 1 and self.x == player.x
            ):
                debug_print(f"Ghost #{self.id} stays still - player adjacent at ({player.x}, {player.y})")
                # Marque le fantôme comme ayant attaqué pour le prochain tour
                self.just_attacked = True
                return

        # Obtient les mouvements possibles
        moves = self.get_available_moves(map_data)

        if moves:
            # Dessine le sol à l'ancienne position
            Block.Sol(int(self.x), int(self.y), self.size)

            # Choisit un mouvement aléatoire
            dx, dy = random.choice(moves)
            old_pos = (self.x, self.y)
            self.last_pos = old_pos  # Sauvegarde la position actuelle
            self.x += dx
            self.y += dy
            self.has_moved = True  # Marque le fantôme comme ayant bougé
            self.blocked_turns = 0  # Réinitialise le compteur de tours bloqués
            debug_print(f"Ghost #{self.id} moved from {old_pos} to ({self.x}, {self.y})")
            self.draw()
        else:
            self.blocked_turns += 1
            debug_print(f"Ghost #{self.id} has no valid moves available, blocked for {self.blocked_turns} turns")
            if self.blocked_turns > 2:
                # Permet au fantôme de reculer
                if self.last_pos:
                    Block.Sol(int(self.x), int(self.y), self.size)
                    self.x, self.y = self.last_pos
                    self.last_pos = None  # Réinitialise la dernière position pour éviter les boucles infinies
                    self.has_moved = True
                    self.blocked_turns = 0  # Réinitialise le compteur de tours bloqués
                    debug_print(f"Ghost #{self.id} moved back to ({self.x}, {self.y})")
                    self.draw()

    def destroy(self):
        """Détruit le fantôme et le retire du jeu"""
        debug_print(f"Ghost #{self.id} destroyed")
        if self.sprite:
            g.supprimer(self.sprite)
            self.sprite = None
        self.visible = False
        try:
            fantomes.remove(self)
        except ValueError:
            debug_print(f"Ghost #{self.id} already removed")


def readmap():
    players = []
    global fantomes, current_ghost_timer
    fantomes = []

    with open("map0.txt", "r") as file:
        map1 = file.readlines()

    # Lecture des paramètres
    time = int(map1[0].split()[1])
    timerfantome = int(map1[1].split()[1])
    current_ghost_timer = timerfantome  # Initialisation du timer
    debug_print(f"Time: {time}, Timer Fantome: {timerfantome}")

    ethernet_positions = []
    for col in range(0, len(map1) - 3):
        mp = map1[col + 3].strip()
        debug_print(repr(mp))
        BI = len(mp)
        for lig in range(0, len(mp)):
            if mp[lig] == "C":
                Block.Colonne(lig, col, L // BI)
            elif mp[lig] == "M":
                Block.Mur(lig, col, L // BI)
            elif mp[lig] == "E":
                Block.Ethernet(lig, col, L // BI)
                ethernet_positions.append((lig, col))
            elif mp[lig] == " ":
                Block.Sol(lig, col, L // BI)
            elif mp[lig] == "P":
                player = Player(lig, col, L // BI)
                player.timer = time
                players.append(player)
                player.draw()

    ghost_spawn_positions = []
    for x, y in ethernet_positions:
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_x, new_y = x + dx, y + dy
            if (
                0 <= new_x < len(map1[3].strip())
                and 0 <= new_y < len(map1) - 3
                and map1[new_y + 3][new_x] == " "
            ):
                ghost_spawn_positions.append((new_x, new_y, L // BI))

    # Création des deux premiers fantômes si possible
    if len(ghost_spawn_positions) >= 2:
        positions = random.sample(ghost_spawn_positions, 2)
        for x, y, size in positions:
            fantome = Fantome(x, y, size)
            fantomes.append(fantome)

    return players, map1[3:], time, timerfantome, ghost_spawn_positions


# Récupère les joueurs et la carte
players, map_data, time, timerfantome, ghost_spawn_positions = readmap()
player = players[0]  # Le premier joueur

# Boucle principale du jeu
while True:
    # Affiche le nouveau HUD
    player.draw_hud()

    # Récupère la touche pressée
    key = g.recupererTouche()

    # Gestion des mouvements
    if key:  # Seulement si une touche est pressée
        debug_print(f"Key pressed: {key}")
        action_performed = False  # Flag to check if an action was performed

        if key == "Left":
            action_performed = player.move(-1, 0, map_data)
        elif key == "Right":
            action_performed = player.move(1, 0, map_data)
        elif key == "Up":
            action_performed = player.move(0, -1, map_data)
        elif key == "Down":
            action_performed = player.move(0, 1, map_data)
        elif key == "space":
            if len(player.active_bombs) < player.max_bombs:
                bomb = Bomb(player.x, player.y, player.size, player)
                player.active_bombs.append(bomb)
                action_performed = True
        elif key == "Escape":
            break

        if action_performed:
            player.update_timer()
            player.check_ghost_collision()  # Vérifie les collisions après chaque mouvement

    # Gestion des bombes
    player.update_bombs(map_data)

    # Gestion des fantômes
    if current_ghost_timer <= 0:  # Le timer est arrivé à zéro
        debug_print("\n=== Ghost Spawn Cycle ===")
        debug_print(f"Current active ghosts: {len(fantomes)}")

        # Création de deux nouveaux fantômes
        if len(ghost_spawn_positions) >= 2:
            positions = random.sample(ghost_spawn_positions, 2)
            for x, y, size in positions:
                fantome = Fantome(x, y, size)
                fantome.show()  # Le rendre visible immédiatement
                fantomes.append(fantome)
                debug_print(f"Spawned new ghost #{fantome.id} at ({x}, {y})")

        current_ghost_timer = timerfantome  # Réinitialise le timer
        debug_print(f"Ghost timer reset to {timerfantome}")
        debug_print(f"Global timer: {player.timer}")
        debug_print("=== End Spawn Cycle ===\n")

    # Décrémenter le timer des fantômes si une action est effectuée
    if key and action_performed:
        current_ghost_timer -= 1
        debug_print(f"Ghost timer: {current_ghost_timer}")

        # Déplacement des fantômes
        for fantome in fantomes:
            if fantome.visible:
                fantome.has_moved = False
                fantome.move(map_data)

    # Rafraîchit l'affichage
    g.actualiser()
    g.pause(0.05)  # Petit délai pour contrôler la vitesse du jeu

# fermeture fenêtre
g.fermerFenetre()
