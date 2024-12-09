# CCCCCCCCC
# C   P   C
# CMCMCMCMC
# CMMMM E C
# CCCCCCCCC

# un mur (M)
# une colonne (C)
# une prise ethernet (E)
# Pour les cases vides
# le bomber (P)
# un fantôme (F)
# un upgrade (U)
# une bombe (B)

base_player = [1, 1]

def plateau():
    plateau = [
        ["C", "C", "C", "C", "C", "C", "C", "C", "C"],
        ["C", " ", " ", " ", "P", " ", " ", " ", "C"],
        ["C", "M", "C", "M", "C", "M", "C", "M", "C"],
        ["C", "M", "M", "M", "M", " ", "E", " ", "C"],
        ["C", "C", "C", "C", "C", "C", "C", "C", "C"],
    ]
    for i in range(len(plateau)):
        for j in range(len(plateau[i])):
            print(plateau[i][j], end="")
        print()
    return plateau