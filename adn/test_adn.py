import pytest 
import adn

#PYTHONPATH=.. python -m pytest nom du fichier ou . (répertoire courant)
#python 

#print(adn.remplir_tableau("AT","AG",1,1,2))

def test_tableau():
    assert adn.remplir_tableau("AT","AG",1,1,2)==[[(0, (0, 0)), (-2, (0, 0))], [(-2, (0, 0)), (1, (0, 0))]]
    assert adn.remplir_tableau("ATA","AA",1,1,2)==[[(0, (0, 0)), (-2, (0, 0)), (-4, (0, 1))], [(-2, (0, 0)), (1, (0, 0)), (-1, (1, 1))]]
    

