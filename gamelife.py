import pygame as pg 
import argparse
import sys
import logging 

#fonction de lecture des arguments entrés
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

#permet de compter le nombre de voisins vivants d'une cellule
def nb_voisin_vivant(tab,i,j): 
    res=0 #contient le nombre de voisins à la fin de l'exécution
    for ligne in range(i-1,i+2): 
        for colonne in range(j-1,j+2):
            if 0<=ligne<len(tab) and 0<=colonne<len(tab[0]): #permet de traiter les cas des cellules sur les extrémités 
                if (ligne,colonne)!=(i,j):
                    if tab[ligne][colonne]==1: #si une cellule vivante est détectée en voisins
                        res=res+1
    return res 

#fonction permettant l'écriture du motif final dans le fichier f
def writeend(tab,f): 
    for i in range(len(tab)):
        for j in range(len(tab._tab[0])):
            f.write(str(tab._tab[i][j]))
        f.write('\n') #pour aller à la ligne dans l'écriture 

#classe du tableau de toutes les cellules du jeu
class Tab: 

    #fonction de definition de ce tableau comme liste de liste
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
    
    #fonction longueur directement créée pour la classe tableau
    def __len__(self): 
        return len(self._tab)
    
    #fonction permettant de mettre un jour le tableau lors d'une étape
    def update_tab(self):  
        tabstock=self._tab.copy() #sert de base pour mettre à jour le tableau sans que ses premières modifications impactent les suivantes
        for i in range(len(self._tab)):
            for j in range(len(self._tab[0])):
                nb=nb_voisin_vivant(tabstock,i,j) #on applique l'algorithme game of life en fonction du nombre de voisins vivants
                if tabstock[i][j]==1:
                    if nb<2:
                        self._tab[i][j]=0
                    elif nb>3:
                        self._tab[i][j]=0
                else:
                    if nb==3:
                        self._tab[i][j]=1

    #fonction permettant d'appliquer la précédente sur un nombre précis d'étapes
    def update_step(self,STEPS): 
        step=0
        while step<STEPS:
            if step<STEPS:
                self.update_tab()
                step=step+1

#classe de l'utilisation de pygame
class Display:
    
    #fonction de définition de ses attributs 
    def __init__(self,SCREENWIDTH,SCREENHEIGHT,WHITE): 
        pg.init()
        self.clock = pg.time.Clock() #horloge du jeu 
        self.screen = pg.display.set_mode( (SCREENWIDTH, SCREENHEIGHT) )  #quadrillage du jeu dont les dimensions sont entrées par le joueur 
        self.screen.fill( WHITE )
        self.Flag=True #variable permettant l'arrêt ou la suite du jeu

    #fonction permettant de récupérer les commandes de l'utilisateur à chaque boucle
    def process_events(self): 
        for event in pg.event.get():
            if event.type == pg.KEYDOWN: #s'il appuie sur Q la partie s'arrête
                if event.key == pg.K_q: 
                    self.Flag=False
            if event.type == pg.QUIT: #s'il appuie sur la croix, la partie s'arrête
                self.Flag=False 

    #fonction permettant de dessiner l'état actuel du tableau de cellules
    def draw(self,tab,TAILLECAR,WHITE,BLACK): 
        self.screen.fill( WHITE ) #on repart de 0 pour redessiner le tableau
        for i in range(len(tab._tab[0])):
            for j in range(len(tab)):
                if tab._tab[j][i]==1: #si la cellule est vivante
                    carre = pg.Rect(i*TAILLECAR,j*TAILLECAR,TAILLECAR, TAILLECAR) #on la dessine avec les pas adaptés
                    pg.draw.rect(self.screen, BLACK, carre)

    #permet d'update le display après un passage dans la boucle
    def update_pygame(self,FPS,TAILLECAR,WHITE,BLACK,tab): 

        self.clock.tick(FPS) #l'horloge fonctionne au rythme de FPS entré par l'utilisateur
        self.process_events() #on récupère les commandes de l'utilisateur pour éventuellement arrêter le jeu
        self.draw(tab,TAILLECAR,WHITE,BLACK) #puis on dessine l'état actuel
        pg.display.update() #et on l'update avec pygame

def main(): #fonction principale contrôlant l'évolution du jeu

    args=read_args() #récupération des arguments

    #Definition des CONSTANTES a partir des arguments 
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
    if args.g__debug: #si le mode debug est activé
        logger.setLevel(logging.DEBUG)

    if args.d: #si le mode affichage est activé 
        logger.info('Le mode affichage est active')
        logger.debug('Lancement de pygame')
        play=Display(SCREENWIDTH,SCREENHEIGHT,WHITE)
    
    with open('gamelife.txt','r') as f: #on ouvre le fichier d'entrée et on récupère ses données
        logger.info('Ouverture du fichier gamelife.txt et recuperation des donnees')
        logger.debug('Lecture du fichier et recuperation des donnees')
        tab=Tab(f) #ses données sont placés dans tab
    
    if args.d: #en mode affichage 
        logger.info('Affichage de l evolution des cellules. Presser Q ou la croix pour quitter')
        logger.debug('Debut de la boucle d affichage de l evolution des cellules')
        while play.Flag==True: #on exécute un nombre infini d'étapes jusqu'à que l'utilisateur ordonne d'arrêter 

            tab.update_tab() #on met à jour le tableau
            play.update_pygame(FPS,TAILLECAR,WHITE,BLACK,tab) #et on met à jour pygame

    else: #sans mode affichage
        logger.info('Simulation de l evolution des cellules sur ' + str(STEPS) + ' etapes') 
        logger.debug('Debut de la simulation de l evolution des cellules')
        tab.update_step(STEPS) #on réalise un nombre fini d'étapes 

    logger.debug('Fin de l evolution des cellules') 

    with open('gamsortie.txt','w') as f: #on ouvre le fichier de sortie 
        logger.info('Ecriture du motif final dans le fichier gamesortie.txt')
        logger.debug('Ecriture dans le fichier de sortie du motif final ')
        writeend(tab,f) #et on y écrit le tableau final retenu 
    
    logger.info('Execution du programme terminee')
    logger.debug('Fin du programme')

main()
quit()

#tab=[[0,1,0],[0,0,0],[1,0,1]]
#print(nb_voisin_vivant(tab,2,2))