import pygame as pg 
import argparse
import sys
import logging 

def read_args():

    parser = argparse.ArgumentParser(description='Arguements du jeu')
    parser.add_argument('--width', type=int, help="Longueur du quadrillage",default=800)
    parser.add_argument('--height', type=int, help="Hauteur du quadrillage",default=600)
    parser.add_argument('-f', type=int, help="Nombre de frames par seconde",default=10)
    parser.add_argument('-m', type=int, help="Nombre d'étapes de la simulation",default=20)

    parser.add_argument('-d', help='Affichage de pygame', action='store_true')

    args = parser.parse_args()
    return args

def nb_voisin_vivant(tab,i,j):
    res=0
    for ligne in range(i-1,i+2):
        for colonne in range(j-1,j+2):
            if 0<=ligne<len(tab) and 0<=colonne<len(tab[0]): 
                if (ligne,colonne)!=(i,j):
                    if tab[ligne][colonne]==1:
                        res=res+1
    return res 

def draw_screen(TAILLECAR,tab,WHITE,BLACK):
    screen.fill( WHITE )
    for i in range(len(tab)):
        for j in range(len(tab[0])):
            if tab[i][j]==1:
                carre = pg.Rect(i*TAILLECAR,j*TAILLECAR,TAILLECAR, TAILLECAR)
                pg.draw.rect(screen, BLACK, carre)

def update_tab(tab):
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


args=read_args() 


SCREENWIDTH=args.width
SCREENHEIGHT=args.height
TAILLECAR=10
FPS=args.f
BLACK=(0,0,0)
WHITE=(255,255,255)
STEPS=args.m

Flag=True
step=0

if args.d:
    pg.init()
    clock = pg.time.Clock()
    screen = pg.display.set_mode( (SCREENWIDTH, SCREENHEIGHT) )  #Création du quadrillage
    screen.fill( WHITE )

    
with open('gamelife.txt','r') as f:
    tab=[]
    i=0
    for line in f:
        line=line.rstrip('\n')
        tab.append([])
        for nb in line:
            tab[i].append(int(nb))
        i=i+1
    
if args.d:
    while Flag==True:
        clock.tick(FPS)

        update_tab(tab)

        for event in pg.event.get():
            if event.type == pg.KEYDOWN: 
                if event.key == pg.K_q:
                    Flag=False
            if event.type == pg.QUIT:
                Flag=False

        draw_screen(TAILLECAR,tab,WHITE,BLACK)
        pg.display.update()

else:
    while step<STEPS:
        if step<STEPS:
            update_tab(tab)
            step=step+1
    
with open('gamsortie.txt','w') as f:
    for i in range(len(tab)):
        for j in range(len(tab[0])):
            f.write(str(tab[i][j]))
        f.write('\n')

quit()

#tab=[[0,1,0],[0,0,0],[1,0,1]]
#print(nb_voisin_vivant(tab,2,2))