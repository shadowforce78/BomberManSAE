from tkiteasy import *


class Draw:
    """
    Classe utilitaire pour le rendu graphique
    Centralise toutes les fonctions de dessin du jeu
    """

    @staticmethod
    def Colonne(g, x, y, c):
        g.dessinerRectangle(x * c, y * c, c, c, "DarkSlateGray")
        g.dessinerLigne(x * c, y * c, x * c, y * c + c, "black")
        g.dessinerLigne(x * c, y * c, x * c + c, y * c, "black")
        g.dessinerLigne(x * c, y * c + c, x * c + c, y * c + c, "black")
        g.dessinerLigne(x * c + c, y * c, x * c + c, y * c + c, "black")
        g.dessinerLigne(x * c, y * c + c, x * c + c, y * c, "black")
        g.dessinerLigne(x * c, y * c, x * c + c, y * c + c, "black")

    @staticmethod
    def Mur(g, x, y, c):

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

    @staticmethod
    def Sol(g, x, y, c):
        g.dessinerRectangle(x * c, y * c, c, c, "tan")
        g.dessinerLigne(x * c, y * c, x * c + c, y * c, "brown")
        g.dessinerLigne(x * c, y * c + (c // 2), x * c + c, y * c + (c // 2), "brown")
        g.dessinerLigne(
            x * c, y * c + (c // 1.3), x * c + c, y * c + (c // 1.3), "brown"
        )
        g.dessinerLigne(
            x * c, y * c + (c // 3.5), x * c + c, y * c + (c // 3.5), "brown"
        )

    @staticmethod
    def Ethernet(g, x, y, c):

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

    @staticmethod
    def Player(g, x, y, size):
        """Dessine le sprite du joueur"""
        center_x = x * size + size / 2
        center_y = y * size + size / 2
        sprite = g.dessinerDisque(center_x, center_y, size / 2, "Yellow")

        # Yeux
        eye_radius = size / 10
        eye_offset = size / 6
        for dx in (-eye_offset, eye_offset):
            g.dessinerDisque(center_x + dx, center_y - eye_offset, eye_radius, "Black")

        # Bouche
        mouth_width = size / 3
        mouth_height = size / 10
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
        return sprite

    @staticmethod
    def Ghost(g, x, y, size):
        """Dessine le sprite d'un fantôme avec plus de détails et sans bugs"""
        center_x = x * size + size / 2
        center_y = y * size + size / 2

        # Corps principal (forme de goutte inversée)
        ghost_body = g.dessinerDisque(center_x, center_y, size / 2, "purple")

        # Base ondulée (plusieurs segments)
        wave_height = size / 6
        wave_width = size / 4
        base_y = center_y + size / 2

        for i in range(5):
            start_x = center_x - size / 2 + i * wave_width
            end_x = start_x + wave_width
            if i % 2 == 0:
                g.dessinerLigne(start_x, base_y, end_x, base_y - wave_height, "purple")
            else:
                g.dessinerLigne(start_x, base_y - wave_height, end_x, base_y, "purple")

        # Yeux
        eye_radius = size / 8
        eye_offset = size / 5
        eye_y = center_y - size / 8

        for dx in (-eye_offset, eye_offset):
            # Blanc des yeux
            g.dessinerDisque(center_x + dx, eye_y, eye_radius, "white")
            # Pupilles
            g.dessinerDisque(center_x + dx, eye_y, eye_radius / 2, "red")

        return ghost_body

    @staticmethod
    def PowerUp(g, x, y, size, powerup_type):
        """Dessine un power-up"""
        colors = {"range": "cyan", "life": "lime green"}
        center_x = x * size + size / 2
        center_y = y * size + size / 2
        return g.dessinerRectangle(
            center_x - size / 4,
            center_y - size / 4,
            size / 2,
            size / 2,
            colors[powerup_type],
        )

    @staticmethod
    def Bomb(g, x, y, size):
        """Dessine une bombe"""
        center_x = x * size + size / 2
        center_y = y * size + size / 2

        # Corps de la bombe
        bomb_sprite = g.dessinerDisque(center_x, center_y, size / 2.5, "black")

        # Mèche
        fuse_width = size / 6
        fuse_height = size / 3
        fuse_sprite = g.dessinerRectangle(
            center_x - fuse_width / 2,
            center_y - fuse_height,
            fuse_width,
            fuse_height,
            "white",
        )
        return bomb_sprite, fuse_sprite
