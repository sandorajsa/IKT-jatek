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
elerhetoFegyverek = [] #lehetne esetleg karakter classban
elerhetoHealek = 0
width = os.get_terminal_size().columns #lehetne kezdetnél megkérni hogy resizolja az ablakot és utána többet ne
szobaid = "startRoom"

roomFirst = {
    1: True,
    4: True,
    9: True,
    10: True,
    13: True,
    15: True,
    16: True,
    18: True,
    20: True
}

quests = {
    "gyogyszer": False,
    "segitseg": True,
    "gyerekek": False,
    "epuletKulcs": False,
    "varosKulcs": False,
    "letra": False
}
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

#Game

def gamestart(): #kilepes
    oppOlvas()
    fegyverOlvas()
    os.system("cls")
    commands = ["Outback","Új játék", "Folytatás"]
    choice = curses.wrapper(menu, commands)
    if choice == commands[1]:
        newgame()
    elif choice == commands[2]:
        # try:
            load()
        # except:
        #     commands = ["Nem találtunk előző játékmentést, szeretnél új játékot kezdeni?", "Igen", "Nem"]
        #     choice = curses.wrapper(menu, commands)
        #     if choice == "Nem":
        #         return
        #     else:
        #         newgame()

def tutorial(): #heal vasarlas, kivalasztas, pontok kesz
    print("Az ehhez hasonló olvasnivalókat a 'space' gomb megnyomásával tudod átlépni de a idővel is továbblép".center(width))
    print("Nyomd meg az 'space'-t a továbblépéshez".center(width))
    var(9999)
    commands = ["A játékunkben ehhez hasonló választésokkal találkozol amit a nyilakkal tudsz navigálni és az enter lenyomásával tudod megerősíteni", "Tovább", "Tovább"]
    choice = curses.wrapper(menu, commands)
    print(f"{bcolors.WARNING}Egy szobában találtad magad egy robottal szemben{bcolors.ENDC}".center(width))
    print("A hátizsákodban kutatva egy fegyvert találsz".center(width))
    print(f"{bcolors.FAIL}A robot ellened fordul{bcolors.ENDC}".center(width))
    print(f"{bcolors.OKGREEN} Az ilyen helyzetekben Outbackben egy menü fogad itt tudsz életerőt regenerálni, fegyvert választani az enter lenyomásával{bcolors.ENDC}".center(width))
    var(99)
    fightSystem(opponents[0])
    print("A harc közben jelentős mennyiségű életerőt vesztettél, a játék során gyógyszertárakba is be tudsz térni ahol gyógyító tárgakat tudsz venni".center(width))
    print("Az ellenfelek legyőzésével pontokat szerzel amiket többek közt itt is el tudsz költeni".center(width))
    jatekos.Points += 1000
    var(99)
    healthBuy()
    print("A játék automatikus mentéssel rendelkezik ami minden szoba elején ment így sosem kell aggódnod, hogy játékállásod elveszik".center(width))
    var(6)

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
    if szam == "Könnyű":
        jatekos = karakter(gamertag, 100, 15, 4, 0, 0)
    elif szam == "Közepes":
        jatekos = karakter(gamertag, 75, 10, 3, 0, 0)
    elif szam == "Nehéz":
        jatekos =karakter(gamertag, 50, 5, 2, 0, 0)
    save()
    startRoom()

def startRoom():
    szobaid = 0
    save()
    commands = ["A város zárt kapuja előtt állsz. Merre haladsz tovább?","Bal ", "Előre" , "Jobb"]
    userinput = curses.wrapper(menu, commands)
    if userinput == commands[1]:
        room1()
    elif userinput == commands[2]:
        room2()
    elif userinput == commands[3]:
        room3()

def fightSystem(enemy): #itt megkérdezni hogy fightfegyverekből levonni jó e
    fightFegyverek = elerhetoFegyverek
    enemyHp = enemy.Hp
    while jatekos.Hp > 0 and enemyHp > 0:
        commands = ["Kérlek válassz az alábbiak közül", "Támadás", "Gyógyítás"]
        choice = curses.wrapper(menu, commands)
        if choice == commands[1]:
            if len(fightFegyverek) == 0:
                # handFight(enemyHp, enemy)
                os.system("cls")
                print("Mivel nincsen fegyvered kézzel harcolsz.".center(width))
                var(6)
                os.system("cls")
                enemyHp -= jatekos.Dmg
                if enemyHp >= 0:
                    print(f"Az ellenség {jatekos.Dmg} sebzést szenvedett. Jelenlegi életereje: {enemyHp}".center(width))
                    var(6)
                    os.system("cls")
                else:
                    print(f"Az ellenség {jatekos.Dmg} sebzést szenvedett. Jelenlegi életereje: 0".center(width))
                    var(6)
                    os.system("cls")
                print("Az ellenség visszatámad.".center(width))
                var(6)
                os.system("cls")
                jatekos.Hp -= enemy.Dmg
                if jatekos.Hp >= 0:
                    print(f"Sebzést szenvedtél. Jelenlegi életerőd: {jatekos.Hp}".center(width))
                    var(6)
                    os.system("cls")
                else:
                    print("Sebzést szenvedtél. Jelenlegi életerőd: 0".center(width))
                    var(6)
                    os.system("cls")
            else:
                commands = ["Válassz egy fegyvert a támadáshoz"]
                for fegyver in fightFegyverek:
                    commands.append(f"{fegyver.Nev} ({fegyver.Hasznalhato})")
                choice = curses.wrapper(menu, commands)
                if choice == commands[1]:
                    for fegyver in fightFegyverek:
                        if fegyver.Nev == commands[1]:
                #             weaponChoose(fegyver, enemy, enemyHp)
                # elif choice == commands[2]:
                #     for fegyver in fightFegyverek:
                #         if fegyver.Nev == commands[2]:
                #             weaponChoose(fegyver, enemy, enemyHp)
                # elif choice == commands[3]:
                #     for fegyver in fightFegyverek:
                #         if fegyver.Nev == commands[3]:
                #             weaponChoose(fegyver, enemy, enemyHp)
                # elif choice == commands[4]:
                #     for fegyver in fightFegyverek:
                #         if fegyver.Nev == commands[4]:
                #             weaponChoose(fegyver, enemy, enemyHp)
                            if fegyver.Hasznalhato != 0:
                                enemyHp -= fegyver.Dmg
                                print(f"Az ellenség {fegyver.Dmg} sebzést szenvedett. Jelenlegi életereje: {enemyHp}".center(width))
                                var(6)
                                os.system("cls")
                                fegyver.Hasznalhato - 1
                                print("Az ellenség visszatámad.".center(width))
                                var(6)
                                os.system("cls")
                                jatekos.Hp -= enemy.Dmg
                                if jatekos.Hp >= 0:
                                    print(f"Sebzést szenvedtél. Jelenlegi életerőd: {jatekos.Hp}".center(width))
                                    var(6)
                                    os.system("cls")
                                else:
                                    print("Sebzést szenvedtél. Jelenlegi életerőd: 0".center(width))
                                    var(6)
                                    os.system("cls")
                            else:
                                print(f"Sajnos a {fegyver.Nev} ebben a harcban már nem használható.".center(width))
                                var(6)
                                os.system("cls")
        elif choice == commands[2]:
            healthSystem()
    if jatekos.Hp <= 0:
        deathEnd()
    elif enemyHp <= 0:
        jatekos.Points += enemy.Points
        os.system("cls")
        print(f"{enemy.Nev} meghalt.".center(width))
        var(6)
        os.system("cls")

def weaponChoose(fegyver, enemy, enemyHp): #nem vonja le enemyHpból másodjára
    if fegyver.Hasznalhato != 0:
        enemyHp -= fegyver.Dmg
        if enemyHp >= 0:
            print(f"Az ellenség {fegyver.Dmg} sebzést szenvedett. Jelenlegi életereje: {enemyHp}".center(width))
            var(6)
            os.system("cls")
        else:
            print(f"Az ellenség {fegyver.Dmg} sebzést szenvedett. Jelenlegi életereje: 0".center(width))
            var(6)
            os.system("cls")
        fegyver.Hasznalhato - 1
        print("Az ellenség visszatámad.".center(width))
        var(6)
        os.system("cls")
        jatekos.Hp -= enemy.Dmg
        if jatekos.Hp >= 0:
            print(f"Sebzést szenvedtél. Jelenlegi életerőd: {jatekos.Hp}".center(width))
            var(6)
            os.system("cls")
        else:
            print("Sebzést szenvedtél. Jelenlegi életerőd: 0".center(width))
            var(6)
            os.system("cls")
    else:
        print(f"Sajnos a {fegyver.Nev} ebben a harcban már nem használható.".center(width))
        var(6)
        os.system("cls")

def handFight(enemyHp, enemy):
    print("Mivel nincsen fegyvered kézzel harcolsz.".center(width))
    var(6)
    os.system("cls")
    enemyHp -= jatekos.Dmg
    if enemyHp >= 0:
        print(f"Az ellenség {jatekos.Dmg} sebzést szenvedett. Jelenlegi életereje: {enemyHp}".center(width))
        var(6)
        os.system("cls")
    else:
        print(f"Az ellenség {jatekos.Dmg} sebzést szenvedett. Jelenlegi életereje: 0".center(width))
        var(6)
        os.system("cls")
    if enemyHp > 0:
        print("Az ellenség visszatámad.".center(width))
        var(6)
        os.system("cls")
        jatekos.Hp -= enemy.Dmg
        if jatekos.Hp >= 0:
            print(f"Sebzést szenvedtél. Jelenlegi életerőd: {jatekos.Hp}".center(width))
            var(6)
            os.system("cls")
        else:
            print("Sebzést szenvedtél. Jelenlegi életerőd: 0".center(width))
            var(6)
            os.system("cls")

def healthSystem():
    healErtek = 20
    if elerhetoHealek == 0:
        print("Sajnos nincsen elérhető életerő növelőd.".center(width))
        var(6)
        os.system("cls")
    elif jatekos.Hp == 100:
        print("Nincsen szükséged életerő növelésre.".center(width))
        var(6)
        os.system("cls")
    else:
        if jatekos.Hp + healErtek > 100:
            hozzaadandoHp = 100 - jatekos.Hp
            jatekos.Hp += hozzaadandoHp
            print("Életerő feltöltve.".center(width)) 
            print(f"Jelenlegi életerő: {jatekos.Hp}".center(width)) 
            var(6)
            os.system("cls")
        else:
            jatekos.Hp += healErtek
            print("Életerő feltöltve.".center(width))    
            print(f"Jelenlegi életerő: {jatekos.Hp}".center(width))  
            var(6)
            os.system("cls")  

def healthBuy():
    global elerhetoHealek
    print("1000 pont - 1 életerő növelő".center(width))
    print(f"Pontjaid: {jatekos.Points}".center(width))
    var(6)
    os.system("cls")
    commands = ["Veszel életerő növelőt?", "Igen", "Nem"]
    choice = curses.wrapper(menu, commands)
    if choice == commands[1]:
        if jatekos.Points - 1000 < 0:
            print("Nincsen elegendő pontod.".center(width))
            var(6)
            os.system("cls")
            healthBuy()
        else:
            jatekos.Points -= 1000
            elerhetoHealek += 1
            print(f"Életerő növelők száma eggyel megnövelve. Jelenlegi mennyiség: {elerhetoHealek}".center(width))
            var(6)
            os.system("cls")
            healthBuy()

def room1():
    global szobaid, elerhetoHealek
    szobaid = 1
    save()
    commands = ["Nagy szemeteskukák között vagy.", "Körülnézek", "Visszasétálok"]
    choice = curses.wrapper(menu, commands)
    if choice == commands[1]:
        if roomFirst[szobaid] == True:
            roomFirst[szobaid] = False
            print("Két kuka között észreveszel egy alkoholos üveget, az alján még pár cseppel.".center(width))
            var(5)
            print("Nem sokkal arrébb találsz néhány anyagdarabot is.".center(width))
            var(5)
            os.system("cls")
            elerhetoHealek += 1
            print(f"Gratulálok, ezennel feloldottad az életerő növelőket. Jelenlegi mennyiség: {elerhetoHealek} darab".center(width))
            var(5)
            os.system("cls")
        else:
            print("A kukák között már mindent megtaláltál.".center(width))
            var(5)
            os.system("cls")
    startRoom()

def room2():
    global szobaid
    szobaid = 2
    save()
    commands = ["Egy park közepén találtad magad.", "Elmegyek az épületek felé", "Elmegyek a bolt felé", "Visszamegyek"]
    choice = curses.wrapper(menu, commands)
    if choice == commands[1]:
        room4()
    elif choice == commands[2]:
        room5()
    elif choice == commands[3]:
        startRoom()
        
def room3():
    global szobaid
    szobaid = 3
    save()
    commands = ["Egy sikátorba érkezel, ahol furcsa hangokat hallasz.", "Körbenézek", "Visszafutok"]
    choice = curses.wrapper(menu, commands)
    if choice == commands[1]:
        if fegyverek[2] not in elerhetoFegyverek:
            os.system("cls")
            print(f"{bcolors.FAIL}Hirtelen egy vörös macska fut végig az egyik erkélyen.{bcolors.ENDC}".center(width))
            var(5)
            print(f"{bcolors.FAIL}Feletébb aranyos...{bcolors.ENDC}".center(width))
            var(5)
            os.system("cls")
            print(f"Egyszer csak leesik valami az erkélyről és nagy hanggal ér földet.".center(width))
            var(5)
            os.system("cls")
            elerhetoFegyverek.append(fegyverek[2])
            print(f"Gratulálok, ezennel feloldottad a következő fegyvert: {fegyverek[2].Nev} (Használhatóság: {fegyverek[2].Hasznalhato}, Sebzés: {fegyverek[2].Dmg})".center(width))
            var(5)
            os.system("cls")
        else:
            print(f"Mivel nem találsz semmit visszatérsz a kapuhoz.".center(width))
            var(5)
            os.system("cls")
    startRoom()

def room4():
    global szobaid
    szobaid = 4
    save()
    if roomFirst[szobaid] == True:
        roomFirst[szobaid] = False
        print("Az épületek között barangolva végül egy sikátorban kötöttél ki.".center(width))
        var(6)
        print("Éppen visszafordulnál, mikor valami mozgást veszel észre az egyik sarokban.".center(width))
        var(6)
        print("Pár pillanat múlva már feléd rohan a sarokból egy csontváz.".center(width))
        var(6)
        os.system("cls")
        # fightSystem(opponents[1])
        print("Ezt szerencsére megúsztad...".center(width))
        var(6)
        os.system("cls")
    else:
        print("Inkább úgy döntesz nem mész vissza, hisz pontosan tudod mi vár ott...".center(width))
        var(6)
        os.system("cls")
    room2()

def room5():
    global szobaid
    szobaid = 5
    save()
    print("Amint belépsz a boltba, egy hullával találod szemben magad.".center(width))
    var(6)
    print("Épphogy magadhoz térsz, egy sötét alakot veszel észre a sarokban.".center(width))
    var(6)
    print("Másodpercekkel később már a földön vagy, rajtad pedig egy megvadult ember szerű lény.".center(width))
    var(6)
    os.system("cls")
    jatekos.Hp -= 10
    print(f"10 sebzést szenvedtél. Jelenlegi életerőd: {jatekos.Hp} HP".center(width))
    var(6)
    os.system("cls")
    if jatekos.Hp > 0:
        print("Lerúgod magadról majd elkezdesz a falon található lyuk felé futni.".center(width))
        var(6)
        os.system("cls")
        room6()
    else:
        deathEnd()

def room6():
    global szobaid
    szobaid = 6
    save()
    print("Szerencsére sikerül elmenekülnöd a lyukon keresztül,".center(width))
    var(6)
    print("ám a befelé vezető utat már egy eldőlt szekrény torlaszolja el.".center(width))
    var(6)
    os.system("cls")
    commands = ["Körülnézve látod, hogy a bolt raktárában vagy.", "Körülnézek", "Menekülök tovább"]
    choice = curses.wrapper(menu, commands)
    if choice == commands[1]:
        print("Kutakodás közben az egyik polc alatt észreveszel valamit. Kihúzod és jobban megnézed.".center(width))
        var(5)
        os.system("cls")
        elerhetoFegyverek.append(fegyverek[1])
        print(f"Gratulálok, ezennel feloldottad a következő fegyvert: {fegyverek[1].Nev} (Használhatóság: Végtelen, Sebzés: {fegyverek[1].Dmg})".center(width))
        var(5)
        os.system("cls")
        print("Keresgélsz még de nem találsz semmi mást, így továbbmész.".center(width))
        var(5)
        os.system("cls")
    room7()

def room7():
    global szobaid
    szobaid = 7
    save()
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
    save()
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
    global szobaid
    szobaid = 9
    save()
    if roomFirst[szobaid] == True:
        roomFirst[szobaid] = False
        print("Felérsz az emeletre. A szobában egy matracot találsz a földön, rajta egy kisfiúval.".center(width))
        var(5)
        print("Mellette egy férfi térdel.".center(width))
        var(5)
        os.system("cls")
        print(f"{bcolors.OKCYAN}A fiam halálosan beteg. Gyógyszer kell neki, de én nem hagyhatom itt.{bcolors.ENDC}".center(width))
        var(5)
        os.system("cls")
        commands = ["Hozol gyógyszert a kisfiúnak?", "Igen", "Nem"]
        choice = curses.wrapper(menu, commands)
        if choice == commands[1]:
            print(f'{bcolors.OKCYAN}"Köszönöm...A neved?"{bcolors.ENDC}'.center(width))
            var(5)
            print("Megmondod a neved.".center(width))
            var(5)
            print(f'{bcolors.OKCYAN}"Köszönöm {jatekos.Nev}!"{bcolors.ENDC}'.center(width))
            var(5)
            print("Elindulsz gyógyszert keresni.".center(width))
            var(5)
            os.system("cls")
        else:
            quests["segitseg"] = False
            print(f'{bcolors.FAIL}"Sajnálom..nem tehetek mást...Sajnálom!!"{bcolors.ENDC}'.center(width))
            var(5)
            print("Az édesapa egyszer csak rádtámad.".center(width))
            var(5)
            os.system("cls")
            # fightSystem(opponents[5])
            print("Nem tudsz semmi másra gondolni, csak hogy azt tetted amit muszáj volt.".center(width))
            var(5)
            print("Sokkos állapotodban legjobbnak találod ha továbbhaladsz utadon,".center(width))
            var(5)
            print("ezzel a kisfiút halálra ítélve.".center(width))
            var(5)
            os.system("cls")
    else:
        if quests["segitseg"] == True:
            if quests["gyogyszer"] == False:
                print(f'{bcolors.OKCYAN}"A gyógyszer...?"{bcolors.ENDC}'.center(width))
                var(5)
                os.system("cls")
            else:
                if fegyverek[3] not in elerhetoFegyverek:
                    jatekos.Points += 5000
                    print(f'{bcolors.OKCYAN}"Visszajöttél...A gyógyszer?"{bcolors.ENDC}'.center(width))
                    var(5)
                    print("Odanyújtod neki.".center(width))
                    var(5)
                    print(f'{bcolors.OKCYAN}"Köszönöm...cserébe tedd el ezt."{bcolors.ENDC}'.center(width))
                    var(5)
                    print("Egy fegyvert és egy kulcsot nyújt feléd.".center(width))
                    var(5)
                    os.system("cls")
                    elerhetoFegyverek.append(fegyverek[3])
                    quests["varosKulcs"] = True
                    print(f"Gratulálok, ezennel feloldottad a következő fegyvert: {fegyverek[3].Nev} (Használhatóság: {fegyverek[3].Hasznalhato}, Sebzés: {fegyverek[3].Dmg})".center(width))
                    var(5)
                    os.system("cls")
                    print("Elteszed a kulcsot is, bár nem tudod mit nyithat...".center(width))
                    var(5)
                    os.system("cls")
                else:
                    print("Inkább nem zaklatod őket...".center(width))
                    var(5)
                    os.system("cls")
        else:
            print("Nem vagy képes visszatérni az emeletre...".center(width))
            var(5)
            os.system("cls")
    room8()

def room10():
    global szobaid
    szobaid = 10
    save()
    if roomFirst[szobaid] == True:
        roomFirst[szobaid] = False
        print("A családi ház pincéjében találod magad.".center(width))
        var(5)
        print("Éppen elkezdenél körülnézni, mikor egy zombi fut feléd teljes sebességgel.".center(width))
        var(5)
        os.system("cls")
        # fightSystem(opponents[2])
        print("Ahogy a holttest fölött állsz, csak remélheted, hogy a nő nem a ház lakosa volt egykor...".center(width))
        var(5)
        print("Éppen távozni készülsz, mikor észreveszel valamit az egyik sarokban.".center(width))
        var(5)
        os.system("cls")
        elerhetoFegyverek.append(fegyverek[4])
        print(f"Gratulálok, ezennel feloldottad a következő fegyvert: {fegyverek[4].Nev} (Használhatóság: {fegyverek[4].Hasznalhato}, Sebzés: {fegyverek[4].Dmg})".center(width))
        var(5)
        os.system("cls")
    else:
        print("A pincében már mindent felkutattál.".center(width))
        var(5)
        os.system("cls")
    room8()

def room11():
    global szobaid
    szobaid = 11
    save()
    print("Az ajtón átlépve egy gyógyszertárba érkezel".center(width))
    var(5)
    os.system("cls")
    commands = ["Itt biztosan találni gyógyszereket...", "Gyógyszert keresek", "Életerő növelőt veszek", "Továbbmegyek egyenesen", "Visszamegyek"]
    choice = curses.wrapper(menu, commands)
    if choice == commands[1]:
        if quests["gyogyszer"] == False:
            quests["gyogyszer"] = True
            print("A pultok mögött körülnézve többféle gyógyszert is találsz.".center(width))
            var(5)
            print("Mindet elhozod, hiszen jól jöhet.".center(width))
            var(5)
            os.system("cls")
        else:
            print("Már az összes gyógyszert összeszedted.".center(width))
            var(5)
            os.system("cls")
        room11()
    elif choice == commands[2]:
        healthBuy()
        room11()
    elif choice == commands[3]:
        room12()
    else:
        room7()

def room12():
    global szobaid
    szobaid = 12
    save()
    print("Kilépsz, és a gyógyszertár hátsó lerakóhelyénél találod magad.".center(width))
    var(5)
    os.system("cls")
    commands = ["Pár méterre egy 10 emeletes hátsó bejáratát látod.", "Bemegyek", "Körülnézek"]
    choice = curses.wrapper(menu, commands)
    if choice == commands[1]:
        print("Éppen elindulsz az ajtó felé, mikor mögötted megjelenik egy horda zombi.".center(width))
        var(5)
        print("Elkezdesz rohanni.".center(width))
        var(5)
        print("Épphogy belépsz az ajtón, a zombik nagy lendülettel rohannak neki,".center(width))
        var(5)
        print("ezzel a visszautat elzárva.".center(width))
        var(5)
        os.system("cls")
        room13()
    else:
        print("Ahogy kutatsz, észreveszel valamit az egyik ott álló kamion alatt...".center(width))
        var(5)
        os.system("cls")
        elerhetoFegyverek.append(fegyverek[5])
        print(f"Gratulálok, ezennel feloldottad a következő fegyvert: {fegyverek[5].Nev} (Használhatóság: {fegyverek[5].Hasznalhato}, Sebzés: {fegyverek[5].Dmg})".center(width))
        var(5)
        os.system("cls")
        print("Éppen indulnál tovább, mikor egy zombihorda rohan feléd teljes sebességel.".center(width))
        var(5)
        print("Elkezdesz rohanni, de mielőtt a házhoz érnél elkapják a lábad.".center(width))
        var(5)
        jatekos.Hp -= 15
        print(f"15 sebzést szenvedtél. Jelenlegi életerőd: {jatekos.Hp} HP".center(width))
        var(5)
        if jatekos.Hp <= 0:
            deathEnd()
        else:
            print("Szerencsére sikerül elérned az ajtóig, ám azt az annak rohanó zombik torlaszolják el,".center(width))
            var(5)
            print("ezzel eltorlaszolva a visszautat.".center(width))
            var(5)
            os.system("cls")
            room13()

def room13():
    global szobaid
    szobaid = 13
    save()
    if roomFirst[szobaid] == True:
        roomFirst[szobaid] = False
        print("Az épületbe lépve sokkos állapotodban elkezdesz kopogni a legközelebbi ajtón.".center(width))
        var(5)
        print("Egy idős férfi nyit ajtót...".center(width))
        var(5)
        print("fegyvert fogva rád.".center(width))
        var(5)
        os.system("cls")
        print(f'{bcolors.OKGREEN}"Mekkora szerencse, hogy pont megjelentél..."{bcolors.ENDC}'.center(width))
        var(5)
        print(f'{bcolors.OKGREEN}"Lenne egy kérésem hozzád, bár nem éppen vagy abban a helyzetben, hogy visszautasítsd."{bcolors.ENDC}'.center(width))
        var(5)
        print(f'{bcolors.OKGREEN}"Hozd le nekem a két unokámat a 2. emeletről."{bcolors.ENDC}'.center(width))
        var(5)
        print(f'{bcolors.OKGREEN}"Az emeleten van egy férfi, de valahogy úgyis megoldod..."{bcolors.ENDC}'.center(width))
        var(5)
        print("Nincsen más lehetőséged, így elindulsz az épület folyosójára.".center(width))
        var(5)
        os.system("cls")
    else:
        if quests["gyerekek"] == True:
            if quests["epuletKulcs"] == True:
                print("Inkább nem mész vissza...".center(width))
                var(5)
                os.system("cls")
            else:
                print(f'{bcolors.OKGREEN}"Látom elhoztad nekem őket, köszönöm..."{bcolors.ENDC}'.center(width))
                var(5)
                print(f'{bcolors.OKGREEN}"Most vedd el ezt és tűnj el innen!"{bcolors.ENDC}'.center(width))
                var(5)
                quests["epuletKulcs"] = True
                print("A kezedbe nyomott egy kulcsot...".center(width))
                var(5)
                print(f'{bcolors.OKGREEN}"Ezzel ki tudsz jutni..."{bcolors.ENDC}'.center(width))
                var(5)
                os.system("cls")
        else:
            print("A gyerekek nélkül nem mersz visszatérni...".center(width))
            var(5)
            os.system("cls")
    room14()

def room14():
    global szobaid
    szobaid = 14
    save()
    commands = ["Az épület földszinti folyósóján vagy.", "Felmegyek az emeletre", "Bemegyek a lakásba", "Kimegyek a főbejáraton"]
    choice = curses.wrapper(menu, commands)
    if choice == commands[1]:
        room15()
    elif choice == commands[2]:
        room13()
    else:
        if quests["epuletKulcs"] == False:
            print("Zárva...".center(width))
            var(5)
            os.system("cls")
            room14()
        else:
            commands = ["Biztosan kilépsz?", "Igen", "Nem"]
            choice = curses.wrapper(menu, commands)
            if choice == commands[1]:
                room19()
            else:
                room14()

def room15():
    global szobaid, elerhetoHealek
    szobaid = 15
    save()
    commands = ["Az első emeleti folyósóra érkezel.", "Körülnézek", "Felmegyek", "Lemegyek"]
    choice = curses.wrapper(menu, commands)
    if choice == commands[1]:
        if roomFirst[szobaid] == True:
            roomFirst[szobaid] = False
            print("Leskelődés közben észreveszel a földön egy falról leesett elsősegély dobozt.".center(width))
            var(5)
            os.system("cls")
            elerhetoHealek += 1
            print(f"Gratulálok, találtál egy életerő növelőt. Jelenlegi mennyiség: {elerhetoHealek} darab".center(width))
            var(5)
            os.system("cls")
            room15()
        else:
            print("Már mindent megtaláltál ezen az emeleten.".center(width))
            var(5)
            os.system("cls")
            room15()
    elif choice == commands[2]:
        room16()
    else:
        room14()

def room16():
    global szobaid
    szobaid = 16
    save()
    if roomFirst[szobaid] == True:
        roomFirst[szobaid] = False
        print("A második emeletre érsz.".center(width))
        var(5)
        print("Amint fellépsz az utolsó lépcsőfokon, már érted kiről beszélt az idős férfi...".center(width))
        var(5)
        print("Egy bandita lő rád fegyverével, de szerencsére nem talál el...".center(width))
        var(5)
        os.system("cls")
        # fightSystem(opponents[3])
        print("El sem hiszed, hogy sikerült túlélned.".center(width))
        var(5)
        print("Szörnyen érzed magad amiatt amit tettél, de tudod,".center(width))
        var(5)
        print("hogy az életed múlt rajta...".center(width))
        var(5)
        print("Kicsit megnyugszol, majd belépsz a lakásba, ahol a gyerekek vannak.".center(width))
        var(5)
        os.system("cls")
        room17()
    else:
        commands = ["Visszatérsz a második emeleti folyosóra.", "Felmegyek", "Lemegyek"]
        choice = curses.wrapper(menu, commands)
        if choice == commands[1]:
            room18()
        else:
            room15()

def room17():
    global szobaid
    szobaid = 17
    save()
    quests["gyerekek"] = True
    print("A lakásba lépve meglátod a két kisgyereket.".center(width))
    var(5)
    print("Egy 6 év körülinek tűnő kisfiú és a nővére áll veled szemben,".center(width))
    var(5)
    print("félelemmel a szemükben.".center(width))
    var(5)
    print("Elmagyarázod nekik, hogy ki vagy és miért jöttél.".center(width))
    var(5)
    print("A magyarázat hallatán közelebb lépnek hozzád.".center(width))
    var(5)
    print(f'{bcolors.WARNING}"Köszönjük szépen..."{bcolors.ENDC}'.center(width))
    var(5)
    print("Látszólag készen állnak követni téged.".center(width))
    var(5)
    os.system("cls")
    room16()

def room18():
    global szobaid
    szobaid = 18
    save()
    if roomFirst[szobaid] == True:
        roomFirst[szobaid] = False
        print("Felérve a harmadik emeletre mozgásra leszel figyelmes...".center(width))
        var(5)
        print("Ekkor veszed észre a sarokban ülő, fertőzött (valamit mert még nem tudom mi legyen).".center(width))
        var(5)
        print("Amint észrevesz téged rádtámad.".center(width))
        var(5)
        os.system("cls")
        # fightSystem[opponents[2]]
        print("Szerencsére sikerült megölnöd...".center(width))
        var(5)
        os.system("cls")
        commands = ["A lépcső a negyedik emeletre le van szakadva.", "Körülnézek", "Lemegyek"]
        choice = curses.wrapper(menu, commands)
        if choice == commands[1]:
            if fegyverek[6] not in elerhetoFegyverek:
                print("A lépcső romjai között figyelmes leszel valamire.".center(width))
                var(5)
                os.system("cls")
                elerhetoFegyverek.append(fegyverek[6])
                print(f"Gratulálok, ezennel feloldottad a következő fegyvert: {fegyverek[6].Nev} (Használhatóság: {fegyverek[6].Hasznalhato}, Sebzés: {fegyverek[6].Dmg})".center(width))
                var(5)
                os.system("cls")
                room18()
            else:
                print("Mindent megtaláltál már.".center(width))
                var(5)
                os.system("cls")
                room18()
        else:
            room16()
    else:
        commands = ["A lépcső a negyedik emeletre le van szakadva.", "Körülnézek", "Lemegyek"]
        choice = curses.wrapper(menu, commands)
        if choice == commands[1]:
            if fegyverek[6] not in elerhetoFegyverek:
                print("A lépcső romjai között figyelmes leszel valamire.".center(width))
                var(5)
                os.system("cls")
                elerhetoFegyverek.append(fegyverek[6])
                print(f"Gratulálok, ezennel feloldottad a következő fegyvert: {fegyverek[6].Nev} (Használhatóság: {fegyverek[6].Hasznalhato}, Sebzés: {fegyverek[6].Dmg})".center(width))
                var(5)
                os.system("cls")
                room18()
            else:
                print("Mindent megtaláltál már.".center(width))
                var(5)
                os.system("cls")
                room18()
        else:
            room16()

def room19():
    global szobaid
    szobaid = 19
    save()
    commands = ["A ház melletti utcára lépsz ki.", "Körülnézek", "Továbbmegyek"]
    choice = curses.wrapper(menu, commands)
    if choice == commands[1]:
        if fegyverek[7] not in elerhetoFegyverek:
            print("A dobozok között nézelődve egyszercsak szuszogásra leszel figyelmes.".center(width))
            var(5)
            print("Közelebb lépve egy juhászkutyát találsz összekuporodva az egyik dobozban.".center(width))
            var(5)
            os.system("cls")
            elerhetoFegyverek.append(fegyverek[7])
            print("Gratulálok, ezzennel a kutya a társad.".center(width))
            var(5)
            print("Harcokban tudod őt használni, melyekben fegyverként működik.".center(width))
            var(5)
            print(f"(Használhatóság: Végtelen, Sebzés: {fegyverek[7].Dmg})".center(width))
            var(5)
            os.system("cls")
            room19()
        else:
            print("A dobozok környékén már mindent fontosat megtaláltál.".center(width))
            var(5)
            os.system("cls")
            room19()
    else:
        room20()

def room20():
    global szobaid, elerhetoHealek
    szobaid = 20
    save()
    commands = ["A város főterén állsz, szemben egy óriási kapuval.", "Körülnézek", "Elmegyek a kapuhoz", "Elmegyek balra", "Visszamegyek"]
    choice = curses.wrapper(menu, commands)
    if choice == commands[1]:
        if roomFirst[szobaid] == True:
            print("A padok között sétálva az egyiken észreveszel két elsősegély dobozt.".center(width))
            var(5)
            print("Habár nyitva vannak, néhány kötszer még található bennük.".center(width))
            var(5)
            os.system("cls")
            elerhetoHealek += 2
            print(f"Gratulálok, találtál két életerő növelőt. Jelenlegi mennyiség: {elerhetoHealek} darab".center(width))
            var(5)
            os.system("cls")
        else:
            print("Már mindent megtaláltál.".center(width))
            var(5)
            os.system("cls")
        room20()
    elif choice == commands[2]:
        room21()
    elif choice == commands[3]:
        room22()
    else:
        room19()

def room21(): #itt nincsen save hogy lehessen végigvinni
    global szobaid
    szobaid = 21
    print("Ahogy közeledsz a kapuhoz, egyre inkább érzed,".center(width))
    var(5)
    print("hogy amiért eddig harcoltál végre itt van előtted.".center(width))
    var(5)
    print("Ez a kapu jelenti a kijutásodat.".center(width))
    var(5)
    os.system("cls")
    print("A kapu előtt állsz, készen arra, hogy elhagyd ezt a helyet...".center(width))
    var(5)
    print("...ám ekkor érdekes hangot hallassz magad mögül.".center(width))
    var(5)
    print("Hátrafordulva egy óriási mutáns zombit veszel észre.".center(width))
    var(5)
    print("Mikor észrevesz ő is téged, teljes sebességel indul meg feléd.".center(width))
    var(5)
    os.system("cls")
    # fightSystem(opponents[6])
    print("Sikerült megölnöd a zombit, ám a végkimerülés szélén állsz.".center(width))
    var(5)
    print("Ismét a kapu felé veszed az irányt.".center(width))
    var(5)
    os.system("cls")
    if quests["varosKulcs"] == False:
        if quests["letra"] == True:
            print("Ott állva veszed észre, hogy a kapu zárva,".center(width))
            var(5)
            print("az idős férfitől kapott kulcs pedig nem nyitja...".center(width))
            var(5)
            print("Ekkor jut eszedbe a létra...".center(width))
            var(5)
            print("A sikátorban talált létrával sikerül átmásznod a kapun,".center(width))
            var(5)
            print("melynek a másik oldalán kimerülve érsz földet.".center(width))
            var(5)
            os.system("cls")
            gameEnd()
        else:
            print("Ott állva jössz rá, hogy a kiút zárva,".center(width))
            var(5)
            print("neked pedig nincsen kulcsod.".center(width))
            var(5)
            print("Megpróbálsz átmászni, de a kapu túl magas...".center(width))
            var(5)
            print("Kimerülten esel a földre...".center(width))
            var(5)
            print(f"{bcolors.FAIL}Feladod...{bcolors.ENDC}".center(width))
            var(5)
            os.system("cls")
            deathEnd()
    else:
        print("Ott állva veszed észre, hogy a kapu zárva.".center(width))
        var(5)
        print("Kipróbálod az idős férfitől kapott kulcsot ám az nem nyitja...".center(width))
        var(5)
        print("Ekkor jut eszedbe az apukától kapott kulcs.".center(width))
        var(5)
        print("Belehelyezed a kulcslyukba és szerencsére kinyitja.".center(width))
        var(5)
        print("Átlépsz a kapun és kimerülten esel a földre.".center(width))
        var(5)
        os.system("cls")
        gameEnd()

def room22():
    global szobaid
    szobaid = 22
    save()
    commands = ["Ismét egy sikátorba lépsz.", "Körülnézek", "Visszamegyek"]
    choice = curses.wrapper(menu, commands)
    if choice == commands[1]:
        if quests["letra"] == False:
            quests["letra"] = True
            print("A sikátor falai közt barangolva egy létrára leszel figyelmes.".center(width))
            var(5)
            print("Gondolván, hogy még jól jöhet, elhozod.".center(width))
            var(5)
            os.system("cls")
        else:
            print("Már mindent megtaláltál.".center(width))
            var(5)
            os.system("cls")
        room22()
    else:
        room20()

def gameEnd():
    print("Sikerült kijutnod a városból...".center(width))
    var(5)
    print(f"{bcolors.FAIL}de vajon mi vár a város falain kívül?{bcolors.ENDC}".center(width))
    var(5)
    os.system("cls")
    print(f"JÁTÉK VÉGE\n".center(width))
    var(2)
    print(f"Elért pontszám: {jatekos.Points}".center(width))
    var(2)
    print(f"Megszerzett fegyverek: {len(elerhetoFegyverek)}/{len(fegyverek)}".center(width))
    var(10)
    os.system("cls")
    endMenu()

def deathEnd():
    print(f"{bcolors.FAIL}MEGHALTÁL{bcolors.ENDC}\n".center(width))
    var(2)
    print(f"Elért pontszám: {jatekos.Points}".center(width))
    var(2)
    print(f"Megszerzett fegyverek: {len(elerhetoFegyverek)}/{len(fegyverek)}".center(width))
    var(10)
    os.system("cls")
    endMenu()

def endMenu():
    commands = ["Válassz az alábbiak közül", "Új játék", "Mentés betöltése", "Kilépés"]
    choice = curses.wrapper(menu, commands)
    if choice == commands[1]:
        gamestart()
    elif choice == commands[2]:
        pass
    else:
        exit()

def save():
    global jatekos
    f = open("save.txt", "a", encoding = "UTF-8")
    f.write(jatekos.Nev)
    f.write("\n")
    global jhp
    f.write(str(jatekos.Hp))
    f.write("\n")
    global szobaid
    f.write(str(szobaid))
    f.write("\n")
    global elerhetoFegyverek
    f.write(str(elerhetoFegyverek))
    f.write(jatekos.Points)
    f.close()

def load():
    f = open("save.txt", "r", encoding = "UTF-8")
    global jatekos
    jatekos = karakter
    jatekos.Nev = f.readline().strip()
    jatekos.Hp = f.readline().strip()
    global szobaid
    szobaid = f.readline().strip()
    global elerhetoFegyverek
    elerhetoFegyverek = f.readline().strip()
    jatekos.Points = f.readline().strip()
    f.close()
    szobak = [startRoom,room1, room2, room3, room4, room5, room6, room7]
    szobak[int(szobaid)]()
