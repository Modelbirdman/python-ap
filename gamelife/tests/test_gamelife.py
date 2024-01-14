import pytest
import gamelife
from pathlib import Path

def test_nbvoisins():
    tab=[[0,1,0],[0,0,0],[1,0,1]]
    assert gamelife.nb_voisin_vivant(tab,1,1)==3
    tab2=[[0,1,0],[1,0,1],[1,1,1]]
    assert gamelife.nb_voisin_vivant(tab2,2,2)==2

def test_update():
    path=Path(Path.cwd()/'tests'/'gametest.txt')
    with open(path,'r') as f:
        tab=gamelife.Tab(f)
    assert tab._tab==[[0,1,0],[0,0,1],[1,1,1]]
    tab.update_tab()
    assert tab._tab==[[0,0,0],[0,0,1],[0,1,1]]


