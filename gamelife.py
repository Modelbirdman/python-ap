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
    parser.add_argument('-g--debug',help='Debug mode', action='store_true')

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

def draw_screen(TAILLECAR,tab,WHITE,BLACK,screen):
    screen.fill( WHITE )
    for i in range(len(tab[0])):
        for j in range(len(tab)):
            if tab[j][i]==1:
                carre = pg.Rect(i*TAILLECAR,j*TAILLECAR,TAILLECAR, TAILLECAR)
                pg.draw.rect(screen, BLACK, carre)


def process_events(Flag):
    for event in pg.event.get():
            if event.type == pg.KEYDOWN: 
                if event.key == pg.K_q:
                    Flag=False
            if event.type == pg.QUIT:
                Flag=False
    return Flag 

def pygame_init(SCREENWIDTH,SCREENHEIGHT,WHITE):
    pg.init()
    clock = pg.time.Clock()
    screen = pg.display.set_mode( (SCREENWIDTH, SCREENHEIGHT) )  #Création du quadrillage
    screen.fill( WHITE )
    Flag=True
    return clock,screen,Flag
    
def writeend(tab,f):
    for i in range(len(tab)):
        for j in range(len(tab._tab[0])):
            f.write(str(tab._tab[i][j]))
        f.write('\n')

def draw(tab,TAILLECAR,WHITE,BLACK,screen):
    screen.fill( WHITE )
    for i in range(len(tab._tab[0])):
        for j in range(len(tab)):
            if tab._tab[j][i]==1:
                carre = pg.Rect(i*TAILLECAR,j*TAILLECAR,TAILLECAR, TAILLECAR)
                pg.draw.rect(screen, BLACK, carre)

def update_pygame(clock,FPS,Flag,TAILLECAR,WHITE,BLACK,screen,tab):

    clock.tick(FPS)
    Flag=process_events(Flag)
    draw(tab,TAILLECAR,WHITE,BLACK,screen)
    pg.display.update()

    return Flag 

class Tab:

    def __init__(self, f):
        tab=[]
        i=0
        for line in f:
            line=line.rstrip('\n')
            tab.append([])
            for nb in line:
                tab[i].append(int(nb))
            i=i+1
        self._tab=tab
    
    def __repr__(self):
        return f"{self._tab}"
    
    def __len__(self):
        return len(self._tab)
    
    
    def update_tab(self):
        tabstock=self._tab.copy()
        for i in range(len(self._tab)):
            for j in range(len(self._tab[0])):
                nb=nb_voisin_vivant(tabstock,i,j)
                if tabstock[i][j]==1:
                    if nb<2:
                        self._tab[i][j]=0
                    elif nb>3:
                        self._tab[i][j]=0
                else:
                    if nb==3:
                        self._tab[i][j]=1

    def update_step(self,STEPS):
        step=0
        while step<STEPS:
            if step<STEPS:
                self.update_tab()
                step=step+1
     
    
    
def main(): 

    args=read_args() 

    SCREENWIDTH=args.width
    SCREENHEIGHT=args.height
    TAILLECAR=10
    FPS=args.f
    BLACK=(0,0,0)
    WHITE=(255,255,255)
    STEPS=args.m

    #Console pour afficher les logs
    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler(sys.stderr)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.info('Pour jouer en mode debug, ajouter l argument -g--debug lors du lancement du jeu')
    if args.g__debug:
        logger.setLevel(logging.DEBUG)

    if args.d:
        logger.info('Le mode affichage est active')
        logger.debug('Lancement de pygame')
        clock,screen,Flag=pygame_init(SCREENWIDTH,SCREENHEIGHT,WHITE)
    
    with open('gamelife.txt','r') as f:
        logger.info('Ouverture du fichier gamelife.txt et recuperation des donnees')
        logger.debug('Lecture du fichier et recuperation des donnees')
        tab=Tab(f)
    
    if args.d:
        logger.info('Affichage de l evolution des cellules. Presser Q ou la croix pour quitter')
        logger.debug('Debut de la boucle d affichage de l evolution des cellules')
        while Flag==True:

            tab.update_tab()
            Flag=update_pygame(clock,FPS,Flag,TAILLECAR,WHITE,BLACK,screen,tab)

    else:
        logger.info('Simulation de l evolution des cellules sur ' + str(STEPS) + ' etapes')
        logger.debug('Debut de la simulation de l evolution des cellules')
        tab.update_step(STEPS)

    logger.debug('Fin de l evolution des cellules') 

    with open('gamsortie.txt','w') as f:
        logger.info('Ecriture du motif final dans le fichier gamesortie.txt')
        logger.debug('Ecriture dans le fichier de sortie du motif final ')
        writeend(tab,f)
    
    logger.info('Execution du programme terminee')
    logger.debug('Fin du programme')

main()
quit()

#tab=[[0,1,0],[0,0,0],[1,0,1]]
#print(nb_voisin_vivant(tab,2,2))