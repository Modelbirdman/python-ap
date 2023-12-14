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
            insert=


