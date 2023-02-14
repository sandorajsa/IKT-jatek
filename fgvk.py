import curses
import os
import time
import random
from osztalyok import *
import keyboard
import threading
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

opponents = []
fegyverek =  []
elerhetoFegyverek = []
elerhetoHealek = 0
width = os.get_terminal_size().columns
szobaid = "startRoom"
room9Elso = True
gyogyszer = False
# def inventory():
#     if keyboard.is_pressed('i'):
#         os.system("cls")
#         commands = ["Hátizsákod"]
#         choice = curses.wrapper(menu, commands)
#         if choice == commands[1]:
#             pass
#         else:
#             pass
def var(ido):
    startido = time.time()
    elteltido = 0
    while elteltido < int(ido):
        elteltido = time.time() - startido
        if keyboard.is_pressed('space'):
            time.sleep(0.5)
            break


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
# nem mukodik
# def  escmenu():
#     curses.endwin()
#     os.system("cls")
#     commands = ["Menü", "Folytatás", "Mentés", "Új játék", "Kilépés", "Segitség"]
#     choice = curses.wrapper(menu, commands)
#     if choice == commands[1]:
#         pass
#     elif choice == commands[2]:
#         save()
#     elif choice == commands[3]:
#         newgame()
#     elif choice == commands[4]:
#         os.exit()
#     elif choice == commands[5]:
#         print("Segitség").center(width)
#     else:
#         os.exit()

# keyboard.add_hotkey('esc', escmenu)
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
    commands = ["Outback","Új játék", "Folytatás"]
    choice = curses.wrapper(menu, commands)
    if choice == commands[1]:
        newgame()
    elif choice == commands[2]:
        try:
            load()
        except:
            commands = ["Nem találtunk előző játékmentést, szeretnél új játékot kezdeni?", "Igen", "Nem"]
            choice = curses.wrapper(menu, commands)
            if choice == "Nem":
                return
            else:
                newgame()

def tutorial():
    print("Az ehhez hasonló olvasnivalókat a 'space' gomb megnyomásával tudod átlépni de a idővel is továbblép")
    print("Nyomd meg az 'space'-t a továbblépéshez")
    var(9999)
    print(f"{bcolors.WARNING}Egy szobában találtad magad egy robottal szemben{bcolors.ENDC}".center(width))
    print("A hátizsákodban kutatva egy fegyvert találsz".center(width))
    print(f"{bcolors.FAIL}A robot ellened fordul{bcolors.ENDC}")
    print(f"{bcolors.OKGREEN} Az ilyen helyzetekben Outbackben egy menü fogad itt tudsz életerőt regenerálni, fegyvert választani{bcolors.ENDC}")
    ()

def newgame():
    global gamertag, jhp, jdmg, jrng, jatekos
    gamertag = ""
    while gamertag == "":
        gamertag = input("Elsőként add meg miként szólítsunk:\n".center(width))
        os.system("cls")
    commands = ["Játszottál már korábban?", "Igen", "Nem"]
    choice = curses.wrapper(menu, commands)
    if choice == commands[1]:
        pass
    else:
        tutorial()
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
    keyboard.add_hotkey('s', save())  
    startRoom()

def startRoom():
    szobaid = 0
    keyboard.add_hotkey('s', save())
    commands = ["A város zárt kapuja előtt állsz. Merre haladsz tovább?","Bal ", "Előre" , "Jobb"]
    userinput = curses.wrapper(menu, commands)
    if userinput == commands[1]:
        room1()
    elif userinput == commands[2]:
        room2()
    elif userinput == commands[3]:
        room3()

def fightSystem(enemy):
    fightFegyverek = elerhetoFegyverek
    enemyHp = enemy.Hp
    while jatekos.Hp != 0 or enemyHp != 0:
        if len(fightFegyverek) == 0:
            pass
        else:
            commands = ["Válassz egy fegyvert a támadáshoz"]
            for fegyver in fightFegyverek:
                commands.append(fegyver.Nev)
            choice = curses.wrapper(menu, commands)
            if choice == commands[1]:
                for fegyver in fightFegyverek:
                    if fegyver.Nev == commands[1]:
                        pass
                    else:
                        enemyHp - jatekos.Dmg
                        os.system("cls")
                        print(f"Az ellenség {jatekos.Dmg} sebzést szenvedett. Jelenlegi életereje: {enemyHp}")
            
def healthSystem():
    healErtek = 20
    if elerhetoHealek == 0:
        os.system("cls")
        text = "Sajnos nincsen elérhető életerő növelőd."
        rows, columns = os.popen('stty size', 'r').read().split()
        center = int(columns) // 2
        print(" " * (center - len(text) // 2) + text)
    elif jatekos.Hp == 100:
        os.system("cls")
        print("Nincsen szükséged életerő növelésre.")
    else:
        if jatekos.Hp + healErtek > 100:
            hozzaadandoHp = 100 - jatekos.Hp
            jatekos.Hp += hozzaadandoHp
            os.system("cls")
            print("Életerő feltöltve.") 
            print(f"Jelenlegi életerő: {jatekos.Hp}") 
        else:
            jatekos.Hp += healErtek
            os.system("cls")
            print("Életerő feltöltve.")    
            print(f"Jelenlegi életerő: {jatekos.Hp}")     

def room1():
    global szobaid
    szobaid = 1
    global elerhetoHealek
    keyboard.add_hotkey('s', save())
    commands = ["Nagy szemeteskukák között vagy.", "Körülnézek", "Visszasétálok"]
    choice = curses.wrapper(menu, commands)
    if elerhetoHealek == 0:
        if choice == commands[1]:
            os.system("cls")
            print("Két kuka között észreveszel egy alkoholos üveget, az alján még pár cseppel.".center(width))
            print("Nem sokkal arrébb találsz néhány anyagdarabot is.".center(width))
            var(5)
            os.system("cls")
            elerhetoHealek += 1
            os.system("cls")
            print(f"Gratulálok, ezennel feloldottad az életerő növelőket. Jelenlegi mennyiség: {elerhetoHealek} darab".center(width))
            var(4)
            os.system("cls")
            print("A kukáknál már mindent átkutattál így visszaindulsz.".center(width))
            var(4)
            os.system("cls")
            startRoom()
        elif choice == commands[2]:
            startRoom()
    else:
        if choice == commands[1]:
            os.system("cls")
            print("A kukáknál mindent átkutattál, ám semmit nem találtál, így visszaindulsz.".center(width))
            var(4)
            os.system("cls")
            startRoom()
        elif choice == commands[2]:
            startRoom()

def room2():
    global szobaid
    szobaid = 2
    keyboard.add_hotkey('s', save())
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
    global szobaid
    szobaid = 3
    keyboard.add_hotkey('s', save())
    commands = ["Egy sikátorba érkezel, ahol furcsa hangokat hallasz.", "Körbenézek", "Visszafutok"]
    choice = curses.wrapper(menu, commands)
    if choice == commands[1]:
        os.system("cls")
        print(f"{bcolors.FAIL}Hirtelen egy vörös macska fut végig az egyik erkélyen.{bcolors.ENDC}".center(width))
        print(f"{bcolors.FAIL}Feletébb aranyos...{bcolors.ENDC}".center(width))
        var(8)
        os.system("cls")
        print(f"Mivel nem találsz semmit visszatérsz a kapuhoz.".center(width))
        var(4)
        os.system("cls")
        startRoom()
    elif choice == commands[2]:
        startRoom()

def room4(): #lehetne itt kutya (fegyverként működne)
    global szobaid
    szobaid = 4
    keyboard.add_hotkey('s', save())
    print("Az épületek között barangolva végül egy sikátorban kötöttél ki.".center(width))
    print("Sajnos az út innen csak visszafelé vezet.".center(width))
    var(6)
    os.system("cls")
    room2()

def room5():
    global szobaid
    szobaid = 5
    keyboard.add_hotkey('s', save())
    print("Amint belépsz a boltba, egy hullával találod szemben magad.".center(width))
    print("Épphogy magadhoz térsz, egy sötét alakot veszel észre a sarokban.".center(width))
    var(6)
    os.system("cls")
    print("Másodpercekkel később már a földön vagy, rajtad pedig egy megvadult ember szerű lény.".center(width))
    var(6)
    os.system("cls")
    jatekos.Hp -= 10
    print(f"10 sebzést szenvedtél. Jelenlegi életerőd: {jatekos.Hp}".center(width))
    var(6)
    os.system("cls")
    print("Lerúgod magadról majd elkezdesz a falon található lyuk felé futni.".center(width))
    var(6)
    os.system("cls")
    room6()


def room6():
    global szobaid
    szobaid = 6
    keyboard.add_hotkey('s', save())
    print("Szerencsére sikerül elmenekülnöd a lyukon keresztül,".center(width)) 
    print("ám a befelé vezető utat már egy eldőlt szekrény torlaszolja el.".center(width))
    var(6)
    os.system("cls")
    commands = ["Körülnézve látod, hogy a bolt raktárában vagy.", "Körülnézek", "Menekülök tovább"]
    choice = curses.wrapper(menu, commands)
    if choice == commands[1]:
        print("Kutakodás közben az egyik polc alatt észreveszel valamit. Kihúzod és jobban megnézed.".center(width))
        var(3)
        os.system("cls")
        #át kell írni majd késre
        print(f"Gratulálok, ezennel feloldottad a következő fegyvert: {fegyverek[0].Nev} (Használhatóság: {fegyverek[0].Hasznalhato}, Sebzés: {fegyverek[0].Dmg})".center(width))
        var(5)
        os.system("cls")
        elerhetoFegyverek.append(fegyverek[0])
        commands = ["Keresgélsz még de nem találsz semmi mást.", "Továbbmegyek"]
        choice = curses.wrapper(menu, commands)
        if choice == commands[1]:
            room7()
    elif choice == commands[2]:
        room7()

def room7():
    global szobaid
    szobaid = 7
    keyboard.add_hotkey('s', save())
    print("Ismét az utcákon találod magad.".center(width))
    var(4)
    os.system("cls")
    commands = ["Jobbra egy családi házat, szemben egy gyógyszertárat látsz.", "Elmegyek jobbra", "Elmegyek előre"]
    choice = curses.wrapper(menu, commands)
    if choice == commands[1]:
        room8()
    else:
        room11()

def room8():
    global szobaid
    szobaid = 8
    keyboard.add_hotkey('s', save())
    print("A családi ház előterébe lépsz.".center(width))
    var(4)
    os.system("cls")
    commands = ["Vezet egy lépcső lefele és egy felfele.", "Felmegyek", "Lemegyek", "Kimegyek"]
    choice = curses.wrapper(menu, commands)
    if choice == commands[1]:
        room9()
    elif choice == commands[2]:
        room10()
    else:
        room7()

def room9():
    global szobaid, room9Elso
    szobaid = 8
    keyboard.add_hotkey('s', save())
    if room9Elso == True:
        print("Felérsz az emeletre. A szobában egy matracot találsz a földön, rajta egy kisfiúval.".center(width))
        print("Mellette egy férfi térdel.".center(width))
        var(6)
        os.system("cls")
        print('"A fiam halálosan beteg. Gyógyszer kell neki, de én nem hagyhatom itt."'.center(width))
        var(6)
        os.system("cls")
        commands = ["Hozol gyógyszert a kisfiúnak?", "Igen", "Nem"]
        choice = curses.wrapper(menu, commands)
        if choice == commands[1]:
            print('"Köszönöm...A neved?"'.center(width))
            print("Megmondod a neved.".center(width))
            var(6)
            os.system("cls")
            print(f'"Köszönöm {jatekos.Nev}!"'.center(width))
            print("Elindulsz gyógyszert keresni.".center(width))
            var(6)
            os.system("cls")
            room9Elso = False
            room8()
    else:
        if gyogyszer == False:
            print('"A gyógyszer...?"'.center(width))
            var(6)
            os.system("cls")
            room8()
        else:
            print('"Visszajöttél...A gyógyszer?"'.center(width))
            print("Odanyújtod neki.".center(width))
            var(6)
            os.system("cls")
            print('"Köszönöm...cserébe tedd el ezt."'.center(width))
            print("Egy fegyvert nyújt feléd.".center(width))
            var(6)
            os.system("cls")
            print(f"Gratulálok, ezennel feloldottad a következő fegyvert: {fegyverek[2].Nev} (Használhatóság: {fegyverek[2].Hasznalhato}, Sebzés: {fegyverek[2].Dmg})".center(width))

def room10():
    pass

def room11():
    pass

def gameend():
    print("Game over")

def save():
    f = open("save.txt", "w", encoding = "UTF-8")
    global gamertag
    f.write(gamertag)
    f.write("\n")
    global jhp
    f.write(str(jhp))
    f.write("\n")
    global szobaid
    f.write(str(szobaid))
    f.write("\n")
    global elerhetoFegyverek
    f.write(str(elerhetoFegyverek))
    f.close()

def load():
    f = open("save.txt", "r", encoding = "UTF-8")
    global gamertag
    gamertag = f.readline().strip()
    global jhp
    jhp = f.readline().strip()
    global szobaid
    szobaid = int(f.readline().strip())
    global elerhetoFegyverek
    elerhetoFegyverek = f.readline().strip()
    f.close()
    szobak = [startRoom,room1, room2, room3, room4, room5, room6, room7]
    szobak[szobaid]()
    keyboard.add_hotkey('s', save())
    szobaid()
