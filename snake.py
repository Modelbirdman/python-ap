import pygame as pg 
import argparse
import sys
import logging 
import re as re


#Fonction d'ajout et test des arguments
def read_args():
   
   #Ajout des arguments
   parser = argparse.ArgumentParser(description='Arguements du jeu snake')
   parser.add_argument('--bg-color-1', help="La première couleur du quadrillage",default=(255,255,255))
   parser.add_argument('--bg-color-2', help="La deuxième couleur du quadrillage",default=(0,0,0))
   parser.add_argument('--width', type=int, help="Longueur du quadrillage",default=400)
   parser.add_argument('--height', type=int, help="Hauteur du quadrillage",default=300)
   parser.add_argument('--fps', type=int, help="Nombre de frames par seconde",default=5)
   parser.add_argument('--fruit-color', help="La couleur du fruit",default=(255,0,0))
   parser.add_argument('--snake-color', help="La couleur du serpent",default=(0,255,0))
   parser.add_argument('--snake-length', type=int, help="Taille du snake",default=3)
   parser.add_argument('--tile-size', type=int, help="Taille du carreau",default=20)

   parser.add_argument('--gameover-on-exit', help='A flag.', action='store_true')
   parser.add_argument('-g--debug',help='Debug mode', action='store_true')

   parser.add_argument('--high-scores-file',help='le chemin d accès au fichier high-score',default=str($HOME/".snake_scores.txt"))
   

   args = parser.parse_args()

   #Test des arguments

   if args.snake_length < 2:
       raise ValueError("La taille du snake doit etre strictement superieure à 1")
   if args.snake_color==args.fruit_color:
       raise ValueError("Le fruit et le snake doivent avoir des couleurs differentes")
   if args.width%args.tile_size!=0:
       raise ValueError("La longueur doit etre un multiple de la taille des carres")
   if args.height%args.tile_size!=0:
       raise ValueError("La hauteur doit etre un multiple de la taille des carres")
   if args.width/args.tile_size<20:
       raise ValueError("La longueur est minimum de 20 colonnes")
   if args.height/args.tile_size<12:
       raise ValueError("La hauteur est minimum de 12 lignes")
   
   return(args)

#fonction contenant la boucle principale
def main():
    #Démarrage de la partie
    pg.init()

    clock = pg.time.Clock()

    #récupération des arguments
    args=read_args()

    #Console pour afficher les logs
    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler(sys.stderr)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    if args.g__debug:
        logger.setLevel(logging.DEBUG)

    logger.debug('Start main loop.')

    logger.info('Pour jouer en mode debug, ajouter l argument -g--debug lors du lancement du jeu')
    logger.info('New game')

    #Initialisation des CONSTANTES à partir des arguments
    COLORS,SCREENWIDTH,SCREENHEIGHT=(args.bg_color_1,args.width,args.height)
    FPS=args.fps
    BLACK =args.bg_color_2
    RED=args.fruit_color
    GREEN=args.snake_color
    SNAKELEN=args.snake_length
    TAILLEREC=args.tile_size

    #Initialisation des variables

    score=0
    vectdir=(1,0) #variable contrôlant la boucle du serpent
    Flag=True #variable contrôlant le passage dans la boucle de jeu
    testfruit=False #variable définissant les passages de boucle où le serpent a mangé le fruit
   
    screen = pg.display.set_mode( (SCREENWIDTH, SCREENHEIGHT) )  #Création du quadrillage
    screen.fill( COLORS )

    snakecor=[]  #Création du snake
    for i in range(SNAKELEN):
        snakecor.append((4*TAILLEREC+i*TAILLEREC,10*TAILLEREC))

    fruit=(3*TAILLEREC,3*TAILLEREC)  #Création du fruit

#Lancement de la boucle de jeu
    while Flag==True:
       clock.tick(FPS)
       vectdir,Flag=process_events(logger,vectdir,Flag)
       Flag,score,fruit,snakecor=update_display(snakecor,TAILLEREC,vectdir,fruit,screen,COLORS,SCREENWIDTH,SCREENHEIGHT,BLACK,RED,GREEN,score,testfruit,args,logger,Flag)

    pattern= "([a-zA-Z]+):([0-9]+)"
    with open(args.high_scores_file,'r') as f:
        fichier=[]
        for line in f:
            match=re.match(pattern,line)
            fichier.append(match.groups())
            
    with open(args.high_scores_file,'w') as f:
    if fichier==[] or  if len(fichier)<5:
        nom = input()
        print(nom+"="+str(score), file=f)
    else:
        min=score
        nom=""
        for ancienscore in fichier:
            if ancienscore[1]<min:
                min=ancienscore[1]
                nom=ancienscore[0]
        if min<score:
            nom=input()
            print(nom+"="+str(score), file=f)
            




        

                    
            


#Fonction de la boucle des évènements
def process_events(logger,vectdir,Flag):
    for event in pg.event.get():
        #Evénements pour faire bouger le serpent
        if event.type == pg.KEYDOWN: 
            if event.key == pg.K_UP:
                vectdir=(0,-1)
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_DOWN:
                vectdir=(0,1)
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                vectdir=(-1,0)
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RIGHT:
                vectdir=(1,0)
        
        #Evenements pour quitter
        if event.type == pg.KEYDOWN: 
            if event.key == pg.K_q:
                Flag=False
                logger.critical('You quit the game')
                logger.debug('Game over')
        if event.type == pg.QUIT:
            Flag=False
            logger.critical('You quit the game')
            logger.debug('Game over')

    return vectdir,Flag

#Fonction de Mise à jour du serpent
def move_snake(snakecor,TAILLEREC,vectdir):
    snakecor.append((snakecor[-1][0]+TAILLEREC*vectdir[0],snakecor[-1][1]+TAILLEREC*vectdir[1]))
    snakecor.pop(0)

#Fonction mettant à jour et affichant le score
def get_score(testfruit,score):
    if testfruit==True:
        score=score+1 
        testfruit=False 
    pg.display.set_caption("Score: "+str(score))
    return score

#Fonction de mise à jour du jeu si le serpent touche le fruit
def update_fruit(snakecor,fruit,score,TAILLEREC,testfruit,logger):
    if snakecor[-1]==fruit:
        testfruit=True
        pg.display.set_caption("Score: "+str(score))
        if fruit==(3*TAILLEREC,3*TAILLEREC):
            fruit=(15*TAILLEREC,10*TAILLEREC)
            snakecor=[snakecor[0]]+snakecor
        else:
            fruit=(3*TAILLEREC,3*TAILLEREC)
            snakecor=[snakecor[0]]+snakecor
        logger.info('Your score is '+str(score))
        logger.debug('Snake has eaten a fruit')
    return testfruit,fruit,snakecor

     
#Fonction de détection des chocs
def touchside(args,snakecor,SCREENWIDTH,SCREENHEIGHT,vectdir,TAILLEREC,testfruit,logger,Flag):

    #Si le snake se touche lui-même
    for i in range(len(snakecor)-1):
        for j in range(i+1,len(snakecor)):
            if snakecor[i]==snakecor[j] and testfruit==False:
                Flag=False
                logger.critical('The snake touched itself')

    #Détection des extrémités 
    #Si le mode Gameover quand contact avec l'extrémité est activé
    if args.gameover_on_exit:
        if snakecor[-1][0]==SCREENWIDTH and vectdir==(1,0):
            Flag=False
            logger.info('You hit the end of the map')
            logger.debug('Game over')
        if snakecor[-1][0]==0 and vectdir==(-1,0):
            Flag=False
            logger.error('You hit the end of the map')
            logger.debug('Game over')
        if snakecor[-1][1]==SCREENHEIGHT and vectdir==(0,1):
            Flag=False
            logger.error('You hit the end of the map')
            logger.debug('Game over')
        if snakecor[-1][1]==0 and vectdir==(0,-1):
            Flag=False
            logger.error('You hit the end of the map')
            logger.debug('Game over')
 
        

    #Si le mode Gameover quand contact avec l'extrémité n'est pas activé
    else:
        if snakecor[-1][0]==SCREENWIDTH and vectdir==(1,0):
            snakecor[-1]=[0,snakecor[-1][1]]
        if snakecor[-1][0]==-TAILLEREC and vectdir==(-1,0):
            snakecor[-1]=[SCREENWIDTH,snakecor[-1][1]]
        if snakecor[-1][1]==SCREENHEIGHT and vectdir==(0,1):
            snakecor[-1]=[snakecor[-1][0],0]
        if snakecor[-1][1]==-TAILLEREC and vectdir==(0,-1):
            snakecor[-1]=[snakecor[-1][0],SCREENHEIGHT]

    return Flag

#Fonction de dessin du quadrillage
def draw_checkerboard(screen,COLORS,SCREENWIDTH,SCREENHEIGHT,TAILLEREC,BLACK):
    screen.fill( COLORS )
  
    for left in [k for k in range(0,SCREENWIDTH,2*TAILLEREC)]: 
        for top in [k for k in range(0,SCREENHEIGHT,2*TAILLEREC)]:
            rect = pg.Rect(left,top,TAILLEREC, TAILLEREC)
            pg.draw.rect(screen, BLACK, rect)
    for left in [k for k in range(TAILLEREC,SCREENWIDTH,2*TAILLEREC)]:
        for top in [k for k in range(TAILLEREC,SCREENHEIGHT,2*TAILLEREC)]:
            rect = pg.Rect(left,top,TAILLEREC, TAILLEREC)
            pg.draw.rect(screen, BLACK, rect)

#Fonction de dessin du fruit
def draw_fruit(fruit,TAILLEREC,screen,RED):
    fruitrec = pg.Rect(fruit[0],fruit[1],TAILLEREC, TAILLEREC)
    pg.draw.rect(screen,RED, fruitrec)

#Fonction de dessin du snake
def draw_snake(snakecor,TAILLEREC,screen,GREEN):   
    for i in range(len(snakecor)):
        draw=pg.Rect(snakecor[i][0],snakecor[i][1],TAILLEREC,TAILLEREC)
        pg.draw.rect(screen,GREEN,draw)
    pg.display.update()

#Fonction de dessin du jeu
def draw(screen,COLORS,SCREENWIDTH,SCREENHEIGHT,TAILLEREC,BLACK,fruit,RED,snakecor,GREEN):
    draw_checkerboard(screen,COLORS,SCREENWIDTH,SCREENHEIGHT,TAILLEREC,BLACK)
    draw_fruit(fruit,TAILLEREC,screen,RED)
    draw_snake(snakecor,TAILLEREC,screen,GREEN)

#Fonction d'update après un passage dans la boucle
def update_display(snakecor,TAILLEREC,vectdir,fruit,screen,COLORS,SCREENWIDTH,SCREENHEIGHT,BLACK,RED,GREEN,score,testfruit,args,logger,Flag):
    move_snake(snakecor,TAILLEREC,vectdir)
    testfruit,fruit,snakecor=update_fruit(snakecor,fruit,score,TAILLEREC,testfruit,logger)
    draw(screen,COLORS,SCREENWIDTH,SCREENHEIGHT,TAILLEREC,BLACK,fruit,RED,snakecor,GREEN)
    score=get_score(testfruit,score)
    Flag=touchside(args,snakecor,SCREENWIDTH,SCREENHEIGHT,vectdir,TAILLEREC,testfruit,logger,Flag)
    
    return Flag,score,fruit,snakecor

#Execution du programme
main()
quit()


