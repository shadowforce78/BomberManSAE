import tkinter as tk

# un mur (M)
# une colonne (C)
# une prise ethernet (E)
# Pour les cases vides
# le bomberman (P)
# un fantôme (F)
# un upgrade (U)
# une bombe (B)
# une explosion (X)

# La carte sous forme de variable Python
map_data = [
    "CCCCCCCCCCCCCCCCCCCCC",
    "C E                 C",
    "C C C C C C C C C C C",
    "C MMMMMMMMMMMMMMMMM C",
    "C CMCMCMCMCMCMCMCMC C",
    "C MMMMMMMMMMMMMMMMM C",
    "C CMCMCMCMCMCMCMCMC C",
    "C MMMMMMMMMMMMMMMMM C",
    "C CMCMCMCMCMCMCMCMC C",
    "C MMMMMMMMMMMMMMMMM C",
    "C CMCMCMCMCMCMCMCMC C",
    "C        P          C",
    "C CMCMCMCMCMCMCMCMC C",
    "C MMMMMMMMMMMMMMMMM C",
    "C CMCMCMCMCMCMCMCMC C",
    "C MMMMMMMMMMMMMMMMM C",
    "C CMCMCMCMCMCMCMCMC C",
    "C MMMMMMMMMMMMMMMMM C",
    "C CMCMCMCMCMCMCMCMC C",
    "C                 E C",
    "CCCCCCCCCCCCCCCCCCCCC",
]

# Interprétation : convertir chaque ligne en liste pour une manipulation facile
map_grid = [list(row) for row in map_data]

TITLE = "Bomberman"
WIDTH = 675
HEIGHT = 750
FPS = 60

# Variables globales pour la position du joueur
player_x = 0
player_y = 0

# Nouvelles variables globales pour l'ATH
lives = 3
score = 0

# Ajouter après les autres variables globales
current_turn = 1

# Trouver la position initiale du joueur
for y, row in enumerate(map_grid):
    for x, cell in enumerate(row):
        if cell == "P":
            player_x = x
            player_y = y


def draw_hud(canvas):
    """Dessine l'ATH avec les vies, le score et le tour actuel"""
    canvas.create_rectangle(0, HEIGHT - 50, WIDTH, HEIGHT, fill="gray")
    canvas.create_text(50, HEIGHT - 25, text=f"Vies: {lives}", fill="white", font=("Arial", 16))
    canvas.create_text(200, HEIGHT - 25, text=f"Score: {score}", fill="white", font=("Arial", 16))
    canvas.create_text(350, HEIGHT - 25, text=f"Tour: {current_turn}", fill="white", font=("Arial", 16))

def draw_map(canvas, map):
    """Draws a game map on a canvas using colored rectangles."""
    color_map = {
        "C": "black",
        "M": "grey",
        "E": "blue",
        "P": "red",
        "F": "purple",
        "U": "yellow",
        "B": "green",
        "X": "orange",
    }
    for y, line in enumerate(map):
        for x, cell in enumerate(line):
            if cell in color_map:
                canvas.create_rectangle(
                    x * 32, y * 32, x * 32 + 32, y * 32 + 32, fill=color_map[cell]
                )
    # Ajouter l'ATH après avoir dessiné la carte
    draw_hud(canvas)


def move_player(event):
    global player_x, player_y, canvas, current_turn
    new_x, new_y = player_x, player_y

    if event.keysym == "Up":
        new_y -= 1
    elif event.keysym == "Down":
        new_y += 1
    elif event.keysym == "Left":
        new_x -= 1
    elif event.keysym == "Right":
        new_x += 1

    # Vérifier si le déplacement est valide
    if (
        0 <= new_x < len(map_grid[0])
        and 0 <= new_y < len(map_grid)
        and map_grid[new_y][new_x] != "C"
        and map_grid[new_y][new_x] != "M"
        and map_grid[new_y][new_x] != "E"
    ):

        # Effacer l'ancienne position
        map_grid[player_y][player_x] = " "
        # Mettre à jour la nouvelle position
        map_grid[new_y][new_x] = "P"
        player_x, player_y = new_x, new_y

        # Incrémenter le tour après chaque mouvement
        current_turn += 1

        # Redessiner la carte et l'ATH
        canvas.delete("all")
        draw_map(canvas, map_grid)

def blink_bomb(canvas, x, y, color, delay=100):
    """Fait clignoter une bombe avant explosion."""
    for _ in range(3):
        canvas.create_rectangle(
            x * 32, y * 32, x * 32 + 32, y * 32 + 32, fill=color
        )
        canvas.update()
        canvas.after(delay)
        canvas.create_rectangle(
            x * 32, y * 32, x * 32 + 32, y * 32 + 32, fill="green"
        )
        canvas.update()
        canvas.after(delay)

def place_bomb(event):
    global player_x, player_y, canvas, current_turn

    if map_grid[player_y][player_x] == "P":  # Placer une bombe à la position du joueur
        map_grid[player_y][player_x] = "B"
        canvas.delete("all")
        draw_map(canvas, map_grid)

        # Faire clignoter la bombe
        blink_bomb(canvas, player_x, player_y, "green")
        # Faire exploser la bombe après 3 secondes
        canvas.after(3000, explode_bomb, player_x, player_y)

        # Incrémenter le tour après avoir placé une bombe
        current_turn += 1

def explode_bomb(x, y):
    global canvas, player_x, player_y, lives

    # Remplacer les cases affectées par une explosion (X)
    for dy in range(-3, 4):
        if 0 <= y + dy < len(map_grid):
            if map_grid[y + dy][x] != "C":
                map_grid[y + dy][x] = "X"
                if y + dy == player_y and x == player_x:
                    lives -= 1
    for dx in range(-3, 4):
        if 0 <= x + dx < len(map_grid[0]):
            if map_grid[y][x + dx] != "C":
                map_grid[y][x + dx] = "X"
                if y == player_y and x + dx == player_x:
                    lives -= 1

    # Effacer la bombe
    map_grid[y][x] = " "

    canvas.delete("all")
    draw_map(canvas, map_grid)
    
def main():
    global canvas
    root = tk.Tk()
    root.title(TITLE)
    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
    canvas.pack()

    # Lier les touches aux mouvements
    root.bind("<Up>", move_player)
    root.bind("<Down>", move_player)
    root.bind("<Left>", move_player)
    root.bind("<Right>", move_player)
    root.bind("<space>", place_bomb)

    draw_map(canvas, map_grid)
    root.mainloop()


main()