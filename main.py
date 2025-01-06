"""
BomberMan SAE - Jeu d'arcade style BomberMan
Développé dans le cadre de la SAE 1.05

Architecture du jeu:
- Système de grille pour la carte
- Gestion d'entités (joueur, fantômes, power-ups)
- Moteur de jeu avec boucle principale
- Système de collision et de destruction
"""

from tkiteasy import *
import random
import math
from draw import Draw

# Configuration globale
DEBUG_MODE = False


def debug_print(*args, **kwargs):
    if DEBUG_MODE:
        print(*args, **kwargs)


# Initialisation de la fenêtre et des variables globales
L, H = 800, 800
g = ouvrirFenetre(L, H)
fantomes = []
current_ghost_timer = 0
powerups = []

"""
Légende des éléments de la carte:
M = Mur (destructible)
C = Colonne (indestructible) 
E = Prise ethernet (point de spawn des fantômes)
P = Position initiale du joueur
"""


class Block:
    """
    Classe de base pour tous les éléments statiques du jeu
    Gère le rendu graphique des différents types de blocs
    """

    def __init__(self, x, y, c):
        self.x = x
        self.y = y
        self.c = c

    @staticmethod
    def Colonne(x, y, c):
        Draw.Colonne(g, x, y, c)

    @staticmethod
    def Mur(x, y, c):
        Draw.Mur(g, x, y, c)

    @staticmethod
    def Sol(x, y, c):
        Draw.Sol(g, x, y, c)

    @staticmethod
    def Ethernet(x, y, c):
        Draw.Ethernet(g, x, y, c)


class Bomb:
    """
    Système de bombes:
    - Placement sur la grille
    - Détonation temporisée
    - Propagation de l'explosion
    """

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
        debug_print(
            f"New bomb placed at ({x},{y}), will explode at timer {self.explosion_timer}"
        )
        self.draw()

    def draw(self):
        self.sprite, self.fuse_sprite = Draw.Bomb(g, self.x, self.y, self.size)

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
    """
    Gestion des explosions:
    - Calcul de la propagation
    - Destruction des murs
    - Dégâts aux entités
    - Animation en plusieurs phases
    """

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
                        debug_print(
                            f"Ghost #{ghost.id} caught in explosion at ({new_x}, {new_y})"
                        )
                        ghosts_to_destroy.append(ghost)

                tile = self.map_data[new_y][new_x]
                explosion_tiles.add((new_x, new_y))
                debug_print(f"Checking tile at ({new_x}, {new_y}): '{tile}'")

                if tile == "M":
                    walls_destroyed += 1
                    debug_print(
                        f"Destroying wall at ({new_x}, {new_y}). Wall count: {walls_destroyed}"
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
                    debug_print(f"Hit indestructible obstacle at ({new_x}, {new_y})")
                    explosion_tiles.remove((new_x, new_y))
                    break
                else:
                    debug_print(
                        f"Explosion continues through empty space at ({new_x}, {new_y})"
                    )
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
    """
    Mécanique du joueur:
    - Déplacement sur la grille
    - Placement de bombes
    - Système de vie et de score
    - Collection de power-ups
    - Progression de niveau
    """

    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.lives = 3
        self.max_bombs = 1  # Maximum de bombes actives à la fois
        self.active_bombs = []  # Pour stocker les bombes
        self.bomb_range = 3  # Distance des explosions par défaut
        self.lvl = 0
        self.speed = 1
        self.timer = 0  # Sera initialisé avec la valeur du fichier
        self.sprite = None
        self.score = 0
        self.last_collision_check = (
            0  # Nouveau: pour suivre le dernier check de collision
        )

    def draw(self):
        if self.sprite:
            g.supprimer(self.sprite)
        self.sprite = Draw.Player(g, self.x, self.y, self.size)

    def move(self, dx, dy, map_data):
        if self.can_move(dx, dy, map_data):
            debug_print(
                f"Player moving from ({self.x},{self.y}) to ({self.x+dx},{self.y+dy})"
            )
            self.x += dx
            self.y += dy

            # Check for powerups at new position
            for upgrade in powerups:  # Utiliser une copie de la liste
                if int(upgrade.x) == int(self.x) and int(upgrade.y) == int(self.y):
                    upgrade.apply(self)
                    debug_print(f"Player collected powerup at ({self.x}, {self.y})")

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
            g.dessinerRectangle(L//2-(L//6),H//2-(H//3),L//3,H//6,"red")
            g.afficherTexte("Game Over!", L//2, H//2-(H//4), "black", 32)
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
        g.dessinerRectangle(0, 0, L, L//20, "black")
        # Affiche le texte du HUD
        g.afficherTexte(hud_text, L//2, L//40, "white", L//50)

    def update_bombs(self, map_data):
        if self.active_bombs:
            debug_print(
                f"Updating {len(self.active_bombs)} active bombs at timer {self.timer}"
            )
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
            g.dessinerRectangle(L//2-(L//6),H//2-(H//3),L//3,H//6,"white")
            g.afficherTexte("Time's Up!", L//2, H//2-(H//4), "black", 32)
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

    def level_up(self):
        self.lvl += 1
        debug_print(f"Player leveled up to level {self.lvl}")
        if self.lvl >= 4:  # Les bonus commencent au niveau 4
            if self.lvl % 2 == 0:  # Niveau pair
                self.bomb_range += 1
                debug_print(f"Bomb range increased to {self.bomb_range}")
            else:  # Niveau impair
                self.lives += 1
                debug_print(f"Lives increased to {self.lives}")


class Fantome:
    """
    Intelligence artificielle des fantômes:
    - Déplacement aléatoire intelligent
    - Évitement des obstacles et autres fantômes
    - Comportement agressif à proximité du joueur
    - Système de blocage et déblocage
    """

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
        self.last_pos = None  # Pour éviter de revenir en arrière inutilement
        self.visible = False  # État de visibilité du fantôme
        self.next_apparition = 0  # Prochain timer d'apparition
        self.has_moved = (
            False  # Nouvel attribut pour suivre si le fantôme a bougé ce tour
        )
        self.id = len(fantomes)  # Ajouter un identifiant unique
        self.blocked_turns = 0  # Compteur de tours bloqués
        self.just_attacked = False  # New attribute to track attack state
        self.updatestate = False
        debug_print(f"Created ghost #{self.id} at position ({x}, {y})")

    def draw(self):
        if self.sprite:
            g.supprimer(self.sprite)
        if self.visible:  # Dessine seulement si visible
            self.sprite = Draw.Ghost(g, self.x, self.y, self.size)
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
        debug_print(
            f"Ghost #{self.id} checking available moves from ({self.x}, {self.y})"
        )
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
                        debug_print(
                            f"Ghost #{self.id} found position ({new_x}, {new_y}) occupied by Ghost #{f.id}"
                        )
                        occupied = True
                        break

                # Vérifie s'il y a un power-up à cette position
                for upgrade in powerups:
                    if int(upgrade.x) == self.x and int(upgrade.y) == self.y:
                        self.updatestate = True
                        debug_print(
                            f"Ghost #{self.id} meets upgrade at ({new_x}, {new_y})"
                        )
                        break

                if not occupied:
                    moves.append((dx, dy))
                    debug_print(
                        f"Ghost #{self.id} found valid move to ({new_x}, {new_y})"
                    )

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
                debug_print(
                    f"Ghost #{self.id} stays still - player adjacent at ({player.x}, {player.y})"
                )
                # Marque le fantôme comme ayant attaqué pour le prochain tour
                self.just_attacked = True
                return

        # Obtient les mouvements possibles
        moves = self.get_available_moves(map_data)
        if moves:
            # Dessine le sol à l'ancienne position
            Block.Sol(int(self.x), int(self.y), self.size)
            
            # Redessine le power-up si nécessaire à l'ancienne position
            for powerup in powerups:
                if int(powerup.x) == int(self.x) and int(powerup.y) == int(self.y):
                    powerup.draw()
                    break
            
            # Choisit un mouvement aléatoire
            dx, dy = random.choice(moves)
            old_pos = (self.x, self.y)
            self.last_pos = old_pos  # Sauvegarde la position actuelle
            self.x += dx
            self.y += dy
            self.has_moved = True  # Marque le fantôme comme ayant bougé
            self.blocked_turns = 0  # Réinitialise le compteur de tours bloqués
            debug_print(
                f"Ghost #{self.id} moved from {old_pos} to ({self.x}, {self.y})"
            )
            self.draw()
        else:
            self.blocked_turns += 1
            debug_print(
                f"Ghost #{self.id} has no valid moves available, blocked for {self.blocked_turns} turns"
            )
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

        # Création d'un power-up à l'emplacement du fantôme
        if player.lvl % 2 == 0:
            PowerUp(int(self.x), int(self.y), self.size, "life")
        else:
            PowerUp(int(self.x), int(self.y), self.size, "range")
            debug_print(f"PowerUp spawned at ghost position ({self.x}, {self.y})")
        try:
            fantomes.remove(self)
        except ValueError:
            debug_print(f"Ghost #{self.id} already removed")


class PowerUp:
    """
    Système de power-ups:
    - Apparition sur destruction des fantômes
    - Types différents selon le niveau
    - Application d'effets au joueur
    """

    def __init__(self, x, y, size, type):
        self.x = x
        self.y = y
        self.size = size
        self.type = type
        self.sprite = None
        powerups.append(self)  # Ajout à la liste globale
        self.draw()
        debug_print(f"PowerUp of type {self.type} created at ({x}, {y})")

    def draw(self):
        if self.sprite:
            g.supprimer(self.sprite)

        self.sprite = Draw.PowerUp(g, self.x, self.y, self.size, self.type)

    def apply(self, player):
        debug_print(f"Applying powerup {self.type} to player")
        player.lvl += 1
        if self.type == "range":
            player.bomb_range += 1
        elif self.type == "life":
            player.lives += 1
        if self.sprite:
            g.supprimer(self.sprite)
        powerups.remove(self)  # Retrait de la liste globale apply


def readmap():
    """
    Chargement et initialisation de la carte:
    - Lecture du fichier de niveau
    - Création des éléments statiques
    - Placement du joueur et des fantômes initiaux
    """
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
            elif mp[lig] == " " or mp[lig] == "P":
                Block.Sol(lig, col, L // BI)
            if mp[lig] == "P":
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


class InputHandler:
    """
    Gestion des entrées utilisateur:
    - Touches directionnelles pour le mouvement
    - Espace pour poser une bombe
    - Échap pour quitter
    """

    def __init__(self, game_window):
        self.game_window = game_window

    def handle_input(self, player, map_data):
        key = self.game_window.recupererTouche()
        if not key:
            return False

        debug_print(f"Key pressed: {key}")
        action_performed = False

        if key == "Escape":
            return None  # Signal to quit game
        action_map = {"Left": (-1, 0), "Right": (1, 0), "Up": (0, -1), "Down": (0, 1)}

        if key in action_map:
            dx, dy = action_map[key]
            action_performed = player.move(dx, dy, map_data)
        elif key == "space":
            if len(player.active_bombs) < player.max_bombs:
                bomb = Bomb(player.x, player.y, player.size, player)
                player.active_bombs.append(bomb)
                action_performed = True
        return action_performed


class GameEngine:
    """
    Moteur principal du jeu:
    - Boucle de jeu
    - Mise à jour des états
    - Gestion des événements
    - Spawn des fantômes
    - Rendu graphique
    """

    def __init__(self, game_window, map_file="map0.txt"):
        self.game_window = game_window
        self.input_handler = InputHandler(game_window)
        (
            self.players,
            self.map_data,
            self.time,
            self.ghost_timer,
            self.ghost_spawn_positions,
        ) = readmap()
        self.player = self.players[0]
        self.current_ghost_timer = self.ghost_timer
        self.running = True

    def update(self):
        # Affichage HUD
        self.player.draw_hud()

        # Gestion des entrées
        action_performed = self.input_handler.handle_input(self.player, self.map_data)

        if action_performed is None:  # Signal de sortie
            self.running = False
            return
        if action_performed:
            self.handle_turn_actions()

        # Mise à jour des éléments de jeu
        self.player.update_bombs(self.map_data)
        self.manage_ghosts(action_performed)

        # Rafraîchissement
        self.game_window.actualiser()
        self.game_window.pause(0.05)

    def handle_turn_actions(self):
        self.player.update_timer()
        self.player.check_ghost_collision()

    def manage_ghosts(self, action_performed):
        if self.current_ghost_timer <= 0:
            self.spawn_ghosts()
            self.current_ghost_timer = self.ghost_timer

        if action_performed:
            self.current_ghost_timer -= 1
            self.move_ghosts()

    def spawn_ghosts(self):
        debug_print("\n=== Ghost Spawn Cycle ===")
        if len(self.ghost_spawn_positions) >= 2:
            positions = random.sample(self.ghost_spawn_positions, 2)
            for x, y, size in positions:
                fantome = Fantome(x, y, size)
                fantome.show()
                fantomes.append(fantome)
                debug_print(f"Spawned new ghost #{fantome.id} at ({x}, {y})")
        debug_print("=== End Spawn Cycle ===\n")

    def move_ghosts(self):
        for fantome in fantomes:
            if fantome.visible:
                fantome.has_moved = False
                fantome.move(self.map_data)

    def run(self):
        while self.running:
            self.update()


# Modification de la boucle principale
def main():
    """Point d'entrée principal du jeu"""
    engine = GameEngine(g)
    engine.run()
    g.fermerFenetre()


if __name__ == "__main__":
    main()
