# CCCCCCCCC
# C   P   C
# CMCMCMCMC
# CMMMM E C
# CCCCCCCCC

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
