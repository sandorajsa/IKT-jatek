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
width = os.get_terminal_size().columns
szobaid = "startRoom"

roomFirst = {
    4: True,
    9: True,
    10: True,
    13: True,
    15: False,
    16: True
}

quests = {
    "gyogyszer": False,
    "segitseg": True,
    "gyerekek": False,
    "epuletKulcs": False,
    "varosKulcs": False
}
# room4Elso = True
# room9Elso = True
# room10Elso = True
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

def gamestart():
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

def tutorial():
    print("Az ehhez hasonló olvasnivalókat a 'space' gomb megnyomásával tudod átlépni de a idővel is továbblép")
    print("Nyomd meg az 'space'-t a továbblépéshez")
    var(9999)
    print(f"{bcolors.WARNING}Egy szobában találtad magad egy robottal szemben{bcolors.ENDC}".center(width))
    print("A hátizsákodban kutatva egy fegyvert találsz".center(width))
    print(f"{bcolors.FAIL}A robot ellened fordul{bcolors.ENDC}")
    print(f"{bcolors.OKGREEN} Az ilyen helyzetekben Outbackben egy menü fogad itt tudsz életerőt regenerálni, fegyvert választani az enter lenyomásával{bcolors.ENDC}")
    var(99)
    fightSystem(opponents[0])
    print("A játék automatikus mentéssel rendelkezik ami minden szoba elején ment így sosem kell aggódnod, hogy játékállásod elveszik")

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
        jatekos = karakter(gamertag, 100, 15, 4)
    elif szam == "2":
        jatekos = karakter(gamertag, 75, 10, 3)
    elif szam == "3":
        jatekos =karakter(gamertag, 50, 5, 2)
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
        gameend()
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
    else:
        return

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
    var(6)
    os.system("cls")
    commands = ["Veszel életerő növelőt?", "Igen", "Nem"]
    choice = curses.wrapper(menu, commands)
    if choice == commands[1]:
        if jatekos.Points - 1000 < 0:
            print("Nincsen elegendő pontod.".center(width))
            var(6)
            os.system("cls")
            return
        else:
            jatekos.Points -= 1000
            elerhetoHealek += 1
            print(f"Életerő növelők száma eggyel megnövelve. Jelenlegi mennyiség: {elerhetoHealek}".center(width))
            var(6)
            os.system("cls")
            return

def room1():
    global szobaid, elerhetoHealek
    szobaid = 1
    save()
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
    save()
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
    save()
    commands = ["Egy sikátorba érkezel, ahol furcsa hangokat hallasz.", "Körbenézek", "Visszafutok"]
    choice = curses.wrapper(menu, commands)
    if choice == commands[1]:
        if fegyverek[2] not in elerhetoFegyverek:
            os.system("cls")
            print(f"{bcolors.FAIL}Hirtelen egy vörös macska fut végig az egyik erkélyen.{bcolors.ENDC}".center(width))
            print(f"{bcolors.FAIL}Feletébb aranyos...{bcolors.ENDC}".center(width))
            var(8)
            os.system("cls")
            print(f"Egyszer csak leesik valami az erkélyről és nagy hanggal ér földet.".center(width))
            var(4)
            os.system("cls")
            elerhetoFegyverek.append(fegyverek[2])
            print(f"Gratulálok, ezennel feloldottad a következő fegyvert: {fegyverek[2].Nev} (Használhatóság: {fegyverek[2].Hasznalhato}, Sebzés: {fegyverek[2].Dmg})".center(width))
            var(8)
            os.system("cls")
            startRoom()
        else:
            print(f"Mivel nem találsz semmit visszatérsz a kapuhoz.".center(width))
            var(4)
            os.system("cls")
            startRoom()
    elif choice == commands[2]:
        startRoom()

def room4(): #lehetne itt kutya (fegyverként működne)
    global szobaid
    szobaid = 4
    save()
    if roomFirst[szobaid] == True:
        roomFirst[szobaid] = False
        print("Az épületek között barangolva végül egy sikátorban kötöttél ki.".center(width))
        print("Éppen visszafordulnál, mikor valami mozgást veszel észre az egyik sarokban.".center(width))
        var(10)
        os.system("cls")
        print("Pár pillanat múlva már feléd rohan a sarokból egy csontváz.".center(width))
        var(6)
        os.system("cls")
        fightSystem(opponents[1])
        print("Ezt szerencsére megúsztad...".center(width))
        var(6)
        os.system("cls")
        room2()
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
    print("Épphogy magadhoz térsz, egy sötét alakot veszel észre a sarokban.".center(width))
    var(6)
    os.system("cls")
    print("Másodpercekkel később már a földön vagy, rajtad pedig egy megvadult ember szerű lény.".center(width))
    var(6)
    os.system("cls")
    jatekos.Hp -= 10
    print(f"10 sebzést szenvedtél. Jelenlegi életerőd: {jatekos.Hp} HP".center(width))
    var(6)
    os.system("cls")
    print("Lerúgod magadról majd elkezdesz a falon található lyuk felé futni.".center(width))
    var(6)
    os.system("cls")
    room6()


def room6():
    global szobaid
    szobaid = 6
    save()
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
        elerhetoFegyverek.append(fegyverek[1])
        print(f"Gratulálok, ezennel feloldottad a következő fegyvert: {fegyverek[1].Nev} (Használhatóság: {fegyverek[1].Hasznalhato}, Sebzés: {fegyverek[1].Dmg})".center(width))
        var(8)
        os.system("cls")
        commands = ["Keresgélsz még de nem találsz semmi mást.", "Továbbmegyek"]
        choice = curses.wrapper(menu, commands)
        if choice == commands[1]:
            room7()
    elif choice == commands[2]:
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

def room9(): #színes szöveg apukának
    global szobaid
    szobaid = 9
    save()
    if roomFirst[szobaid] == True:
        roomFirst[szobaid] = False
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
        else:
            quests["segitseg"] = False
            print('"Sajnálom..nem tehetek mást...Sajnálom!!"'.center(width))
            var(6)
            os.system("cls")
            print("Az édesapa egyszer csak rádtámad.".center(width))
            var(6)
            os.system("cls")
            fightSystem(opponents[5])
            print("Nem tudsz semmi másra gondolni, csak hogy azt tetted amit muszáj volt.".center(width))
            print("Sokkos állapotodban legjobbnak találod ha továbbhaladsz utadon,".center(width))
            print("ezzel a kisfiút halálra ítélve.".center(width))
            var(10)
            os.system("cls")
    else:
        if quests["segitseg"] == True:
            if quests["gyogyszer"] == False:
                print('"A gyógyszer...?"'.center(width))
                var(6)
                os.system("cls")
            else:
                if fegyverek[3] not in elerhetoFegyverek:
                    print('"Visszajöttél...A gyógyszer?"'.center(width))
                    print("Odanyújtod neki.".center(width))
                    var(6)
                    os.system("cls")
                    print('"Köszönöm...cserébe tedd el ezt."'.center(width))
                    print("Egy fegyvert nyújt feléd.".center(width))
                    var(6)
                    os.system("cls")
                    elerhetoFegyverek.append(fegyverek[3])
                    print(f"Gratulálok, ezennel feloldottad a következő fegyvert: {fegyverek[3].Nev} (Használhatóság: {fegyverek[3].Hasznalhato}, Sebzés: {fegyverek[3].Dmg})".center(width))
                    var(6)
                    os.system("cls")
                else:
                    print("Inkább nem zaklatod őket...".center(width))
                    var(6)
                    os.system("cls")
        else:
            print("Nem vagy képes visszatérni az emeletre...".center(width))
            var(6)
            os.system("cls")
    room8()

def room10():
    global szobaid
    szobaid = 10
    save()
    if roomFirst[szobaid] == True:
        roomFirst[szobaid] = False
        print("A családi ház pincéjében találod magad.".center(width))
        print("Éppen elkezdenél körülnézni, mikor egy nőnek tűnő zombi fut feléd teljes sebességgel.".center(width))
        var(5)
        os.system("cls")
        fightSystem(opponents[2])
        print("Ahogy a holttest fölött állsz, csak remélheted, hogy a nő nem a ház lakosa volt egykor...".center(width))
        var(5)
        os.system("cls")
        print("Éppen távozni készülsz, mikor észreveszel valamit az egyik sarokban.".center(width))
        var(5)
        os.system("cls")
        elerhetoFegyverek.append(fegyverek[4])
        print(f"Gratulálok, ezennel feloldottad a következő fegyvert: {fegyverek[4].Nev} (Használhatóság: {fegyverek[4].Hasznalhato}, Sebzés: {fegyverek[4].Dmg})".center(width))
        var(5)
        os.system("cls")
        room8()
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
    var(6)
    os.system("cls")
    commands = ["Itt biztosan találni gyógyszereket...", "Gyógyszert keresek", "Életerő növelőt veszek", "Továbbmegyek egyenesen", "Visszamegyek"]
    choice = curses.wrapper(menu, commands)
    if choice == commands[1]:
        if quests["gyogyszer"] == False:
            quests["gyogyszer"] = True
            print("A pultok mögött körülnézve többféle gyógyszert is találsz.".center(width))
            print("Mindet elhozod, hiszen jól jöhet.".center(width))
            var(8)
            os.system("cls")
            room11()
        else:
            print("Már az összes gyógyszert összeszedted.".center(width))
            var(8)
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
    var(6)
    os.system("cls")
    commands = ["Pár méterre egy 10 emeletes hátsó bejáratát látod.", "Bemegyek", "Körülnézek"]
    choice = curses.wrapper(menu, commands)
    if choice == commands[1]:
        print("Éppen elindulsz az ajtó felé, mikor mögötted megjelenik egy horda zombi.".center(width))
        print("Elkezdesz rohanni.".center(width))
        var(6)
        os.system("cls")
        print("Épphogy belépsz az ajtón, a zombik nagy lendülettel rohannak neki,".center(width))
        print("ezzel a visszautat elzárva.".center(width))
        var(6)
        os.system("cls")
        room13()
    else:
        print("Ahogy kutatsz, észreveszel valamit az egyik ott álló kamion alatt...".center(width))
        var(6)
        os.system("cls")
        elerhetoFegyverek.append(fegyverek[5])
        print(f"Gratulálok, ezennel feloldottad a következő fegyvert: {fegyverek[5].Nev} (Használhatóság: {fegyverek[5].Hasznalhato}, Sebzés: {fegyverek[5].Dmg})".center(width))
        var(6)
        os.system("cls")
        print("Éppen indulnál tovább, mikor egy zombihorda rohan feléd teljes sebességel.".center(width))
        var(6)
        os.system("cls")
        print("Elkezdesz rohanni, de mielőtt a házhoz érnél elkapják a lábad.".center(width))
        jatekos.Hp -= 15
        print(f"15 sebzést szenvedtél. Jelenlegi életerőd: {jatekos.Hp} HP".center(width))
        var(6)
        os.system("cls")
        if jatekos.Hp <= 0:
            gameend()
        else:
            print("Szerencsére sikerül elérned az ajtóig, ám azt az annak rohanó zombik torlaszolják el,".center(width))
            print("ezzel eltorlaszolva a visszautat.".center(width))
            var(6)
            os.system("cls")
            room13()

def room13():
    global szobaid
    szobaid = 13
    save()
    if roomFirst[szobaid] == True:
        roomFirst[szobaid] = False
        print("Az épületbe lépve sokkos állapotodban elkezdesz kopogni a legközelebbi ajtón.".center(width))
        var(6)
        os.system("cls")
        print("Egy idős férfi nyit ajtót...".center(width))
        print("fegyvert fogva rád.".center(width))
        var(6)
        os.system("cls")
        print('"Mekkora szerencse, hogy pont megjelentél..."'.center(width))
        print('"Lenne egy kérésem hozzád, bár nem éppen vagy abban a helyzetben, hogy visszautasítsd."'.center(width))
        var(6)
        os.system("cls")
        print('"Hozd le nekem a két unokámat a 2. emeletről."'.center(width))
        print('"Tele van a hely zombikkal, de valahogy úgyis megoldod..."'.center(width))
        var(6)
        os.system("cls")
        print("Nincsen más lehetőséged, így elindulsz az épület folyosójára.".center(width))
        var(6)
        os.system("cls")
    else:
        if quests["gyerekek"] == True:
            if quests["epuletKulcs"] == True:
                print('"Inkább nem mész vissza..."'.center(width))
                var(6)
                os.system("cls")
            else:
                print('"Látom elhoztad nekem őket, köszönöm..."'.center(width))
                print('"Most vedd el ezt és tűnj el innen!"'.center(width))
                var(6)
                os.system("cls")
                quests["epuletKulcs"] = True
                print("A kezedbe nyomott egy kulcsot...".center(width))
                print('"Ezzel ki tudsz jutni..."'.center(width))
                var(6)
                os.system("cls")
        else:
            print("A gyerekek nélkül nem mersz visszatérni...".center(width))
            var(6)
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
            var(6)
            os.system("cls")
            room14()
        else:
            room19()

def room15():
    global szobaid, elerhetoHealek
    szobaid = 15
    save()
    commands = ["Az első emeleti folyósóra érkezel.", "Körülnézek", "Feljebb megyek", "Lejjebb megyek"]
    choice = curses.wrapper(menu, commands)
    if choice == commands[1]:
        if roomFirst[szobaid] == False:
            print("Leskelődés közben észreveszel a földön egy falról leesett elsősegély dobozt.".center(width))
            var(6)
            os.system("cls")
            elerhetoHealek += 1
            print(f"Gratulálok, találtál egy életerő növelőt. Jelenlegi mennyiség: {elerhetoHealek} darab".center(width))
            var(4)
            os.system("cls")
            room15()
        else:
            print("Már mindent megtaláltál ezen az emeleten.".center(width))
            var(6)
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
        print("A második emeletre érsz.".center(width))
        var(6)
        os.system("cls")
        print("Amint fellépsz az utolsó lépcsőfokon, már érted miről beszélt az idős férfi...".center(width))
        var(6)
        os.system("cls")
        print("Egy mutáns zombi rohan feléd azonnal, teljes sebességgel.".center(width))
        var(6)
        os.system("cls")
        fightSystem(opponents[6])
        print("El sem hiszed, hogy sikerült legyőznöd.".center(width))
        print("Kicsit megnyugszol, majd belépsz a lakásba, ahol a gyerekek vannak.".center(width))
        var(6)
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
    pass

def room18():
    global szobaid
    szobaid = 18
    save()
    pass

def room19():
    global szobaid
    szobaid = 19
    save()
    pass

def gameend():
    print("Game over".center(width))
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
    f.close()
    szobak = [startRoom,room1, room2, room3, room4, room5, room6, room7]
    szobak[int(szobaid)]()
