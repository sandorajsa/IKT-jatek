# from main import *
from fgvk import *

class karakter:
    def __init__(self):
        self.nev = gamertag
        self.hp = jhp
        self.dmg = jdmg
        self.rng = jrng
        self.money = 0
        self.points = 0
        #ha lehet akkor az első utése utan a karakterunk minden körben kapjon 2dmg-t

class Opp:
    def __init__(self, sor):
        # ajsa csinad meg pls
        adatok = sor.strip().split(";")
        self.nev = adatok[0]
        self.hp = int(adatok[1])
        self.dmg = int(adatok[2])
        self.type = adatok[3]

