import curses
import os
import time
import random
from osztalyok import *

#Basics

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

jrng = 0
opponents = []
fegyverek =  []
elerhetoFegyverek = []
elerhetoHealek = 0
width = os.get_terminal_size().columns

def menu(stdscr,commands):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_RED)
    selected_index = 1

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        for index, command in enumerate(commands):
            x = width//2 - len(command)//2
            y = height//2 - len(commands)//2 + index
            if index == selected_index:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, command)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, command)

        stdscr.refresh()

        c = stdscr.getch()
        if c == curses.KEY_UP:
            selected_index = max(selected_index - 1, 1)
        elif c == curses.KEY_DOWN:
            selected_index = min(selected_index + 1, len(commands) - 1)
        elif c == ord('\n'):
            return commands[selected_index]

def oppOlvas():
    f = open("oppok.txt", "r", encoding="utf-8")
    f.readline()
    for sor in f:
        opponents.append(Opp(sor))
    f.close()

def fegyverOlvas():
    f = open("fegyverek.txt", "r", encoding="utf-8")
    f.readline()
    for sor in f:
        fegyverek.append(Fegyver(sor))
    f.close()

oppOlvas()
fegyverOlvas()

#Game

def gamestart():
    os.system("cls")
    commands = ["Üdvözlünk a 'jaték neve'","Új játék", "Folytatás"]
    choice = curses.wrapper(menu, commands)
    if choice == commands[1]:
        newgame()
    else:
        try:
            f = open("savegame.txt", "r", encoding= "UTF-8")
        except:
            commands = ["Nem találtunk előző játékmentést, szeretnél új játékot kezdeni?", "Igen", "Nem"]
            choice = curses.wrapper(menu, commands)
            if choice == "Nem":
                return
            else:
                newgame()

def newgame():
    global gamertag, jhp, jdmg, jrng, jatekos
    gamertag = input("Elsőként add meg miként szólítsunk:\n".center(width))
    os.system("cls")
    commands = ["Válassz nehézségi fokozatot:","1", "2", "3"]
    szam = curses.wrapper(menu, commands)
    if szam == "1":
        jhp = 100
        jdmg = 15
        jrng = 4
    elif szam == "2":
        jhp = 75
        jdmg = 10
        jrng = 3
    elif szam == "3":
        jhp = 50
        jdmg = 5
        jrng = 2
    jatekos = karakter(gamertag, jhp, jdmg, jrng)
    startRoom()

def startRoom():
    commands = ["A város zárt kapuja előtt állsz. Merre haladsz tovább?","Bal ", "Előre" , "Jobb"]
    userinput = curses.wrapper(menu, commands)
    if userinput == commands[1]:
        room1()
    elif userinput == commands[2]:
        room2()
    elif userinput == commands[3]:
        room3()

# def fightSystem(enemy): #végén fegyverekből újra append elerhetoFegyverekbe
#     fightFegyverek = elerhetoFegyverek
#     enemyHp = enemy.Hp
#     while jatekos.Hp != 0 or enemyHp != 0:
#         if len(fightFegyverek) == 0:
#             pass
#         else:
#             commands = ["Válassz egy fegyvert a támadáshoz"]
#             for fegyver in fightFegyverek:
#                 commands.append(fegyver.Nev)
#             choice = curses.wrapper(menu, commands)
#             if choice == commands[1]:
#                 for fegyver in fightFegyverek:
#                         if fegyver.Nev == commands[1]:

#                     pass
#                 else:
#                     enemyHp - dmg
#                     print(f"Az ellenség {dmg} sebzést szenvedett. Jelenlegi életereje: {enemyHp}")
            
def healthSystem():
    healErtek = 20
    if elerhetoHealek == 0:
        print("Sajnos nincsen elérhető életerő növelőd.")
    elif jatekos.Hp == 100:
        print("Nincsen szükséged életerő növelésre.")
    else:
        if jatekos.Hp + healErtek > 100:
            hozzaadandoHp = 100 - jatekos.Hp
            jatekos.Hp += hozzaadandoHp
            print("Életerő feltöltve.") 
            print(f"Jelenlegi életerő: {jatekos.Hp}") 
        else:
            jatekos.Hp += healErtek
            print("Életerő feltöltve.")    
            print(f"Jelenlegi életerő: {jatekos.Hp}")     

def room1():
    global elerhetoHealek
    commands = ["Nagy szemeteskukák között vagy.", "Körülnézek", "Visszasétálok"]
    choice = curses.wrapper(menu, commands)
    if elerhetoHealek == 0:
        if choice == commands[1]:
            print("Két kuka között észreveszel egy alkoholos üveget, az alján még pár cseppel.".center(width))
            print("Nem sokkal arrébb találsz néhány anyagdarabot is.".center(width))
            time.sleep(8)
            os.system("cls")
            elerhetoHealek += 1
            print(f"Gratulálok, ezennel feloldottad az életerő növelőket. Jelenlegi mennyiség: {elerhetoHealek} darab".center(width))
            time.sleep(4)
            os.system("cls")
            print("A kukáknál már mindent átkutattál így visszaindulsz.".center(width))
            time.sleep(4)
            os.system("cls")
            startRoom()
        elif choice == commands[2]:
            startRoom()
    else:
        if choice == commands[1]:
            print("A kukáknál mindent átkutattál, ám semmit nem találtál, így visszaindulsz.".center(width))
            time.sleep(4)
            os.system("cls")
            startRoom()
        elif choice == commands[2]:
            startRoom()

def room2():
    commands = ["Egy park közepén találtad magad.", "Elmegyek az épületek felé", "Elmegyek a bolt felé", "Visszamegyek"]
    choice = curses.wrapper(menu, commands)
    if choice == commands[1]:
        room4()
    elif choice == commands[2]:
        room5()
    elif choice == commands[3]:
        startRoom()
    else:
        return
        
def room3():
    commands = ["Egy sikátorba érkezel, ahol furcsa hangokat hallasz.", "Körbenézek", "Visszafutok"]
    choice = curses.wrapper(menu, commands)
    if choice == commands[1]:
        print(f"{bcolors.FAIL}Hirtelen egy vörös macska fut végig az egyik erkélyen.{bcolors.ENDC}".center(width))
        print(f"{bcolors.FAIL}Feletébb aranyos...{bcolors.ENDC}".center(width))
        time.sleep(8)
        os.system("cls")
        print(f"Mivel nem találsz semmit visszatérsz a kapuhoz.".center(width))
        time.sleep(4)
        os.system("cls")
        startRoom()

def room4(): #lehetne itt kutya (fegyverként működne)
    print("Az épületek között barangolva végül egy sikátorban kötöttél ki.".center(width))
    print("Sajnos az út innen csak visszafelé vezet.".center(width))
    time.sleep(6)
    os.system("cls")
    room2()

def room5():
    print("Amint belépsz a boltba, egy hullával találod szemben magad.".center(width))
    print("Épphogy magadhoz térsz, egy sötét alakot veszel észre a sarokban.".center(width))
    time.sleep(6)
    os.system("cls")
    print("Másodpercekkel később már a földön vagy, rajtad pedig egy megvadult ember szerű lény.".center(width))
    print("Lerúgod magadról majd elkezdesz a falon található lyuk felé futni.".center(width))
    time.sleep(6)
    os.system("cls")
    room6()


def room6():
    print("Szerencsére sikerül elmenekülnöd a lyukon keresztül,".center(width)) 
    print("ám a befelé vezető utat már egy eldőlt szekrény torlaszolja el.".center(width))
    time.sleep(6)
    os.system("cls")
    commands = ["Körülnézve látod, hogy a bolt raktárában vagy.", "Körülnézek", "Menekülök tovább"]
    choice = curses.wrapper(menu, commands)
    if choice == commands[1]:
        print("Kutakodás közben az egyik polc alatt észreveszel valamit. Kihúzod és jobban megnézed.".center(width))
        time.sleep(3)
        os.system("cls")
        print(f"Gratulálok, ezennel feloldottad a következő fegyvert: {fegyverek[0].Nev} (Használhatóság: {fegyverek[0].Hasznalhato}, Sebzés: {fegyverek[0].Dmg})".center(width))
        time.sleep(5)
        os.system("cls")
        elerhetoFegyverek.append(fegyverek[0])
        commands = ["Keresgélsz még de nem találsz semmi mást.", "Továbbmegyek"]
        choice = curses.wrapper(menu, commands)
        if choice == commands[1]:
            room7()
    elif choice == commands[2]:
        room7()

def room7():
    pass

def gameend():
    print("Game over")