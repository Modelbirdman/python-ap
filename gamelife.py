import pygame as pg 
import argparse
import sys
import logging 

pg.init()
clock = pg.time.Clock()

SCREENWIDTH=800
SCREENHEIGHT=600
FPS=10
BLACK=(0,0,0)
WHITE=(255,255,255)
STEPS=20

Flag=True

screen = pg.display.set_mode( (SCREENWIDTH, SCREENHEIGHT) )  #Création du quadrillage
screen.fill( WHITE )

def nb_voisin_vivant(tab,i,j):
    res=0
    for ligne in range(i-1,i+2):
        for colonne in range(j-1,j+2):
            if 0<=ligne<len(tab) and 0<=colonne<len(tab[0]): 
                if (ligne,colonne)!=(i,j):
                    if tab[ligne][colonne]==1:
                        res=res+1
    return res 
    



with open('gamelife.txt','r') as f:
    tab=[]
    i=0
    for line in f:
        line=line.rstrip('\n')
        tab.append([])
        for nb in line:
            tab[i].append(int(nb))
        i=i+1
    for loop in range(STEPS):
        tabstock=tab.copy()
        for i in range(len(tab)):
            for j in range(len(tab[0])):
                nb=nb_voisin_vivant(tabstock,i,j)
                if tabstock[i][j]==1:
                    if nb<2:
                        tab[i][j]=0
                    elif nb>3:
                        tab[i][j]=0
                else:
                    if nb==3:
                        tab[i][j]=1
                        

#tab=[[0,1,0],[0,0,0],[1,0,1]]
#print(nb_voisin_vivant(tab,2,2))

      

    

while Flag==True:
    clock.tick(10)
    for event in pg.event.get():
        if event.type == pg.KEYDOWN: 
            if event.key == pg.K_q:
                Flag=False
        if event.type == pg.QUIT:
            Flag=False
    pg.display.update()

quit()
