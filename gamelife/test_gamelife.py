import pytest
import gamelife

tab=[[0,1,0],[0,0,0],[1,0,1]]

def test_nbvoisins():
    assert gamelife.nb_voisin_vivant(tab,1,1)==3