# from main import *
from fgvk import *

class karakter:
    def __init__(self, gamerNev, megadottHp, megadottDmg, megadottRng):
        self.Nev = gamerNev
        self.Hp = megadottHp
        self.Dmg = megadottDmg
        self.Rng = megadottRng
        self.Money = 0
        self.Points = 0
        #ha lehet akkor az első utése utan a karakterunk minden körben kapjon 2dmg-t

class Opp:
    def __init__(self, sor):
        adatok = sor.strip().split(";")
        self.Nev = adatok[0]
        self.Hp = int(adatok[1])
        self.Dmg = int(adatok[2])
        self.Type = adatok[3]
        self.Points = int(adatok[4])

class Fegyver:
    def __init__(self, sor):
        adatok = sor.strip().split(";")
        self.Nev = adatok[0]
        self.Hasznalhato = int(adatok[1])
        self.Dmg = int(adatok[2])