import sys
import re
import logging

patseq = ">([a-z_]+)"
patchaine= "[ATGC]*$"
nomseq=""
nomvar=""
seq=""
var=""
i=0

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stderr)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

if __name__ == "__main__": 
#python adn.py<seq_to_align.fasta.txt
    for line in sys.stdin:
        i=i+1
        line=line.rstrip()
        if not line.startswith(';'):
            if re.match(patseq,line) and nomvar!="":
                print(seq)
                print(var)
                seq=""
                var=""
                nomseq=""
                nomvar=""
                logger.info("sequences traitées")
            if re.match(patseq, line):
                if nomseq=="":
                    nomseq=line
                    logger.info("id sequence detectee")
                else:
                    nomvar=line
                    logger.info("id var detecte")
            elif re.match(patchaine, line):
                if seq=="":
                    seq=seq+line
                    logger.info("sequence detectee")
                else:
                    var=var+line
                    logger.info("variant detecte")
            else:
                raise ValueError('la ligne non reconnue est '+str(i))
    if seq!="" and var!="":
        print(seq)
        print(var)



def traitement(nomseq,nomvar,seq,var):
    tableau=[[0 for j in range(len(seq))] for i in range(len(var))]
    for i in range(len(seq)):
        tableau[0][i]=-i
    for j in range(len(var)):
        tableau[j][0]=-i
    for j in range(1,len(var)):
        for i in range(1,len(seq)):
            #gauche=addition et bas=suppression
            insert=tableau[j][i-1]-2
            delete=tableau[j-1][i]-2
            if re.mathc(seq[i],seq[j]):
                sub=tableau[j-1][i-1]+1
            else:
                sub=tableau[j-1][i-1]-1
            tableau[j,i]=max(insert,delete,sub)
    
    depart=[(len(var)-1,len(seq)-1)]
    score=tableau[len(var)-1][len(seq)-1]
    while depart[-1]!=(0,0):
        gauche=tableau[depart[-1][0]-1][depart[-1][1]]
        haut=tableau[depart[-1][0]][depart[-1][1]-1]
        diag=tableau[depart[-1][0]-1][depart[-1][1]-1]
        if max(gauche,haut,diag)==gauche:
            depart.append((depart[-1][0]-1,depart[-1][1]))
            score=score+gauche
        elif max(gauche,haut,diag)==haut:
            depart.append((depart[-1][0],depart[-1][1]-1))
            score=score+haut
        else:
            depart.append((depart[-1][0]-1,depart[-1][1]-1))
            score=score+diag