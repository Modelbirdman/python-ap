import pygame as pg 
import argparse
import sys
import logging 


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

class Fruit:

    def __init__(self, x, y,color,points):
        self._x=x
        self._y =y
        self._color=color
        self._points=points

    def __repr__(self):
        return f"({self._x:.2f} , {self._y:.2f})"
    
    def update(self,snakecor,score,TAILLEREC,testfruit,logger):
        if snakecor[-1]==(self._x,self._y):
            testfruit=True
            pg.display.set_caption("Score: "+str(score))
            if (self._x,self._y)==(3*TAILLEREC,3*TAILLEREC):
                self._x,self._y=15*TAILLEREC,10*TAILLEREC
                snakecor=[snakecor[0]]+snakecor
            else:
                self._x,self._y=3*TAILLEREC,3*TAILLEREC
                snakecor=[snakecor[0]]+snakecor
            logger.info('Your score is '+str(score))
            logger.debug('Snake has eaten a fruit')
        return testfruit,snakecor
    
    def draw(self,TAILLEREC,screen):
        fruitrec = pg.Rect(self._x,self._y,TAILLEREC, TAILLEREC)
        pg.draw.rect(screen,self._color, fruitrec)

class Snake:

    def __init__(self, snakecor,GREEN):
        self._snakecor=snakecor
        self._color=GREEN

    def __repr__(self):
        return f"{self.snakecor}"
    
    #Fonction de Mise à jour du serpent
    def move(self,TAILLEREC,vectdir):
        self._snakecor.append((self._snakecor[-1][0]+TAILLEREC*vectdir[0],self._snakecor[-1][1]+TAILLEREC*vectdir[1]))
        self._snakecor.pop(0)
    

class Factory:

    def __init__(self):
        self._fact=[]

    def declareFruit(self, name, color, points):
        self._fact.append((name,color,points))

    def createFruit(self, name,x,y):
        for fruit in self._fact:
            if fruit[0]==name:
                newfruit=Fruit(x,y,fruit[1],fruit[2])
        return newfruit 
    
    def createSnake(self, length,TAILLEREC,GREEN):
        snakecorinit=[]  #Création du snake
        for i in range(length):
            snakecorinit.append((4*TAILLEREC+i*TAILLEREC,10*TAILLEREC))
    
        snakecor=Snake(snakecorinit,GREEN)
        return snakecor

            

    

    

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
    
    fact=Factory()
    fact.declareFruit('apple',RED,1)
    fruit=fact.createFruit('apple',3*TAILLEREC,3*TAILLEREC)  #Création du fruit
    snakecor=fact.createSnake(SNAKELEN,TAILLEREC,GREEN)

#Lancement de la boucle de jeu
    while Flag==True:
       clock.tick(FPS)
       vectdir,Flag=process_events(logger,vectdir,Flag)
       Flag,score,fruit,snakecor=update_display(snakecor,TAILLEREC,vectdir,fruit,screen,COLORS,SCREENWIDTH,SCREENHEIGHT,BLACK,score,testfruit,args,logger,Flag)

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


#Fonction mettant à jour et affichant le score
def get_score(testfruit,score):
    if testfruit==True:
        score=score+1 
        testfruit=False 
    pg.display.set_caption("Score: "+str(score))
    return score

     
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


#Fonction de dessin du snake
def draw_snake(snakecor,TAILLEREC,screen):   
    for i in range(len(snakecor._snakecor)):
        draw=pg.Rect(snakecor._snakecor[i][0],snakecor._snakecor[i][1],TAILLEREC,TAILLEREC)
        pg.draw.rect(screen,snakecor._color,draw)
    pg.display.update()

#Fonction de dessin du jeu
def draw(screen,COLORS,SCREENWIDTH,SCREENHEIGHT,TAILLEREC,BLACK,fruit,snakecor):
    draw_checkerboard(screen,COLORS,SCREENWIDTH,SCREENHEIGHT,TAILLEREC,BLACK)
    fruit.draw(TAILLEREC,screen)
    draw_snake(snakecor,TAILLEREC,screen)

#Fonction d'update après un passage dans la boucle
def update_display(snakecor,TAILLEREC,vectdir,fruit,screen,COLORS,SCREENWIDTH,SCREENHEIGHT,BLACK,score,testfruit,args,logger,Flag):
    snakecor.move(TAILLEREC,vectdir)
    testfruit,snakecor._snakecor=fruit.update(snakecor._snakecor,score,TAILLEREC,testfruit,logger)
    draw(screen,COLORS,SCREENWIDTH,SCREENHEIGHT,TAILLEREC,BLACK,fruit,snakecor)
    score=get_score(testfruit,score)
    Flag=touchside(args,snakecor._snakecor,SCREENWIDTH,SCREENHEIGHT,vectdir,TAILLEREC,testfruit,logger,Flag)

    return Flag,score,fruit,snakecor

#Execution du programme
main()
quit()


