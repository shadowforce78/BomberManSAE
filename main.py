import tkinter as tk

# un mur (M)
# une colonne (C)
# une prise ethernet (E)
# Pour les cases vides
# le bomber (P)
# un fantôme (F)
# un upgrade (U)
# une bombe (B)

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
HEIGHT = 650

# Variables globales pour la position du joueur
player_x = 0
player_y = 0

# Trouver la position initiale du joueur
for y, row in enumerate(map_grid):
    for x, cell in enumerate(row):
        if cell == "P":
            player_x = x
            player_y = y


def draw_map(canvas, map):
    for y, line in enumerate(map):
        for x, cell in enumerate(line):
            if cell == "C":
                canvas.create_rectangle(
                    x * 32, y * 32, x * 32 + 32, y * 32 + 32, fill="black"
                )
            elif cell == "M":
                canvas.create_rectangle(
                    x * 32, y * 32, x * 32 + 32, y * 32 + 32, fill="grey"
                )
            elif cell == "E":
                canvas.create_rectangle(
                    x * 32, y * 32, x * 32 + 32, y * 32 + 32, fill="blue"
                )
            elif cell == "P":
                canvas.create_rectangle(
                    x * 32, y * 32, x * 32 + 32, y * 32 + 32, fill="red"
                )
            elif cell == "F":
                canvas.create_rectangle(
                    x * 32, y * 32, x * 32 + 32, y * 32 + 32, fill="purple"
                )
            elif cell == "U":
                canvas.create_rectangle(
                    x * 32, y * 32, x * 32 + 32, y * 32 + 32, fill="yellow"
                )
            elif cell == "B":
                canvas.create_rectangle(
                    x * 32, y * 32, x * 32 + 32, y * 32 + 32, fill="green"
                )


def move_player(event):
    global player_x, player_y, canvas
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
    ):

        # Effacer l'ancienne position
        map_grid[player_y][player_x] = " "
        # Mettre à jour la nouvelle position
        map_grid[new_y][new_x] = "P"
        player_x, player_y = new_x, new_y

        # Redessiner la carte
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

    draw_map(canvas, map_grid)
    root.mainloop()


main()
