from fgvk import *
import random
print("Üdvözlünk a játékban")
gamertag = input("Elsőként add meg miként szólítsunk:\n\t")
levels = ["1", "2", "3"]
szam = 0
while szam not in levels:
    szam = input("Adja meg a nehézségi szintet: ")
    if szam == 1:
        jhp = 100
        jdmg = 15
    if szam == 2:
        jhp = 75
        jdmg = 10
    if szam == 3:
        jhp = 50
        jdmg = 5

# 3 diff level 100-15-25 75-10-20 50-5-15
startRoom()
