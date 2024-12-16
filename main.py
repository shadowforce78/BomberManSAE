#coding: utf-8
from tkiteasy import *
import random
import math

# ouverture de fenêtre
g = ouvrirFenetre(800, 800)


# votre programme ICI

class Block:
    def __init__(self, x, y, c):
        self.x = x
        self.y = y
        self.c = c

    def Colonne (x,y,c):
        g.dessinerRectangle(x*c,y*c,c,c,"DarkSlateGray")
        g.dessinerLigne(x*c,y*c,x*c,y*c+c,"black")
        g.dessinerLigne(x*c,y*c,x*c+c,y*c,"black")
        g.dessinerLigne(x*c,y*c+c,x*c+c,y*c+c,"black")
        g.dessinerLigne(x*c+c,y*c,x*c+c,y*c+c,"black")
        g.dessinerLigne(x*c,y*c+c,x*c+c,y*c,"black")
        g.dessinerLigne(x*c,y*c,x*c+c,y*c+c,"black")

    def Mur (x,y,c):
        g.dessinerRectangle(x*c,y*c,c,c,"red")
        g.dessinerLigne(x*c,y*c,x*c,y*c+c,"darkred")
        g.dessinerLigne(x*c,y*c,x*c+c,y*c,"darkred")
        g.dessinerLigne(x*c,y*c+c,x*c+c,y*c+c,"darkred")
        g.dessinerLigne(x*c+c,y*c,x*c+c,y*c+c,"darkred")
        g.dessinerLigne(x*c+(c//2),y*c,x*c+(c//2),y*c+c,"darkred")
        g.dessinerLigne(x*c,y*c+(c//2),x*c+c,y*c+(c//2),"darkred")

    def Sol (x,y,c):
        g.dessinerRectangle(x*c,y*c,c,c,"bisque")
        g.dessinerLigne(x*c,y*c,x*c+c,y*c,"brown")
        g.dessinerLigne(x*c,y*c+(c//1.5),x*c+c,y*c+(c//1.5),"brown")
        g.dessinerLigne(x*c,y*c+(c//3),x*c+c,y*c+(c//3),"brown")

def readmap1 ():
    with open('map0.txt', 'r') as file:
        map1 = file.readlines()
    for col in range(0,len(map1)-3):
        mp = map1[col+3]
        print(mp)
        for lig in range(0,len(mp)):
            if mp[lig] == "C":
                Block.Colonne(lig,col,20)
                #g.dessinerRectangle(lig*20,col*20,20,20,"LightSlateGray")
            elif mp[lig] == "M":
                Block.Mur(lig,col,20)
                #g.dessinerRectangle(lig*20,col*20,20,20,"Aliceblue")
            elif mp[lig] == "E":
                g.dessinerRectangle(lig*20,col*20,20,20,"DarkViolet")
            elif mp[lig] == " ":
                Block.Sol(lig,col,20)
                #g.dessinerRectangle(lig*20,col*20,20,20,"bisque")
            elif mp[lig] == "P":
                g.dessinerRectangle(lig*20,col*20,20,20,"Yellow")


readmap1()

# boucle à vide qui attend un clic
while g.recupererClic() == None:
    continue

# fermeture fenêtre
g.fermerFenetre()