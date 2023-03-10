import keyboard
keyboard.press('f11')
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
jatekos = None
opponents = []
fegyverek =  []
elerhetoFegyverek = [] #lehetne esetleg karakter classban
elerhetoHealek = 0
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
    20: True,
    22: True,
    23: True,
    26: True,
    27: True
}

quests = {
    "gyogyszer": False,
    "segitseg": True,
    "gyerekek": False,
    "epuletKulcs": False,
    "varosKulcs": False,
    "letra": False,
    "kapuKulcs": False
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
            return True
    return True

def kiir(szoba):
    f = open(f"{szoba}.txt", "r", encoding="UTF-8")
    for sor in f: 
        asd = []
        asd = sor.strip().split(';') 
        strtext = asd[0]
        text = strtext.strip().split('+')
        strszin = asd[1]
        szin = strszin.strip().split('+')
        varido = asd[2]
        curses.wrapper(centertext,text,varido, szin)


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

def centertext(stdscr, text=["nincs szoveg:("], varido=6, szin=[""]):#fontos hogy a text legyen lista, amit új sorba akarsz az külön elem legyen szin lehet red, gre, yel, blu, mag, cya, nem muszaj megadni neki semmit
    curses.curs_set(0)
    for index, szin1 in enumerate(szin):
        if szin1 == "red":
            curses.init_pair(index+1, curses.COLOR_RED, curses.COLOR_BLACK)
        elif szin1 == "gre":
            curses.init_pair(index+1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        elif szin1 == "yel":
            curses.init_pair(index+1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        elif szin1 == "blu":
            curses.init_pair(index+1, curses.COLOR_BLUE, curses.COLOR_BLACK)
        elif szin1 == "mag":
            curses.init_pair(index+1, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        elif szin1 == "cya":
            curses.init_pair(index+1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        for index, command in enumerate(text):
            x = width//2 - len(command)//2
            y = height//2 - len(text)//2 + index
            if len(szin) > 1:
                stdscr.attron(curses.color_pair(index+1))
            else:
                stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, command)
            if len(szin) > 1:
                stdscr.attroff(curses.color_pair(index+1))
            else:
                stdscr.attroff(curses.color_pair(1))
        stdscr.refresh()
        if var(varido) == True:
            return

def centerinput(stdscr, text=["nincs szoveg:("], varido=6, szin=[""]):#fontos hogy a text legyen lista, amit új sorba akarsz az külön elem legyen szin lehet red, gre, yel, blu, mag, cya, nem muszaj megadni neki semmit
    curses.curs_set(0)
    for index, szin1 in enumerate(szin):
        if szin1 == "red":
            curses.init_pair(index+1, curses.COLOR_RED, curses.COLOR_BLACK)
        elif szin1 == "gre":
            curses.init_pair(index+1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        elif szin1 == "yel":
            curses.init_pair(index+1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        elif szin1 == "blu":
            curses.init_pair(index+1, curses.COLOR_BLUE, curses.COLOR_BLACK)
        elif szin1 == "mag":
            curses.init_pair(index+1, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        elif szin1 == "cya":
            curses.init_pair(index+1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    while True: 
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        for index, command in enumerate(text):
            x = width//2 - len(command)//2
            y = height//2 - len(text)//2 + index
            if len(szin) > 1:
                stdscr.attron(curses.color_pair(index+1))
            else:
                stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, command)
            if len(szin) > 1:
                stdscr.attroff(curses.color_pair(index+1))
        curses.cbreak()
        curses.echo()
        input = stdscr.getstr(y+1, x).decode("utf-8")
        stdscr.refresh()
        return input

        
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
    commands = ["Outback","Új játék", "Folytatás", "Kilépés"]
    choice = curses.wrapper(menu, commands)
    if choice == commands[1]:
        global roomFirst
        roomFirst = {1: True,4: True,9: True,10: True,13: True,15: True,16: True,18: True,20: True, 22: True, 23: True, 26: True, 27: True}
        global quests
        quests = {"gyogyszer": False,"segitseg": True,"gyerekek": False,"epuletKulcs": False,"varosKulcs": False,"letra": False, "kapuKulcs": False}
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
    else:
        exit()

def tutorial(): #heal vasarlas, kivalasztas, pontok kesz
    global jatekos, elerhetoHealek
    kiir("szovegek/tut1")
    global elerhetoFegyverek
    elerhetoFegyverek.append(fegyverek[0])
    os.system("cls")
    fightSystem(opponents[0])
    text = ["A harc közben jelentős mennyiségű életerőt vesztettél,","a játék során gyógyszertárakba is be tudsz térni ahol"," gyógyító tárgyakat tudsz venni"]#bugos a szöveg
    curses.wrapper(centertext, text, 9)
    text = ["Az ellenségek legyőzésével pontokat szerzel amiket többek közt itt is el tudsz költeni"]
    curses.wrapper(centertext, text, 9)
    os.system("cls")
    healthBuy()
    text = ["A játék automatikusan menti a játékállásod minden szoba elején,","így sosem kell aggódnod, hogy elveszik a játékállásod"]
    curses.wrapper(centertext, text, 9)
    #var(6)
    os.system("cls")
    jatekos.Points = 0
    elerhetoHealek = 0
    elerhetoFegyverek = []
    text = ["Sok sikert a játékban!"]
    szin = ["mag"]
    curses.wrapper(centertext, text, 9, szin)
    os.system("cls")

def newgame():
    global gamertag, jhp, jdmg, jrng, jatekos
    gamertag = ""
    text = ["Kérlek add meg a játékos nevedet:"]
    while gamertag.strip() == "":
        gamertag = curses.wrapper(centerinput, text)
        os.system("cls")
    commands = ["Válassz nehézségi fokozatot:","Könnyű", "Közepes ", "Nehéz "]
    szam = curses.wrapper(menu, commands)
    if szam == commands[1]:
        jatekos = karakter(gamertag, 100, 5, 4)
    elif szam == commands[2]:
        jatekos = karakter(gamertag, 75, 4, 3)
    elif szam == commands[3]:
        jatekos = karakter(gamertag, 50, 3, 2)
    commands = ["Játszottál már korábban?", "Igen", "Nem"]
    choice = curses.wrapper(menu, commands)
    if choice == commands[1]:
        pass
    else:
        tutorial()
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

def fightSystem(enemy): #nem mukodik jol a hasznalhato tobb fegyvernel
    global enemyHp
    fightFegyverek = []
    # for i in range(len(elerhetoFegyverek)):
    #     for j in range(len(fegyverek)):
    #         if elerhetoFegyverek[i].Nev == fegyverek[j].Nev:
    #             hasznal = fegyverek[j].Hasznalhato
    #             elerhetoFegyverek[i].Hasznalhato = hasznal
    for fegyver in elerhetoFegyverek:
        fightFegyverek.append(fegyver)
    enemyHp = enemy.Hp
    while jatekos.Hp > 0 and enemyHp > 0:
        commands = [f"Életerőd: {jatekos.Hp}", "Támadás", "Gyógyítás"]
        choice = curses.wrapper(menu, commands)
        if choice == commands[1]:
            if len(fightFegyverek) == 0:
                enemyHp = handFight(enemyHp, enemy)
            else:
                commands = ["Válassz egy fegyvert a támadáshoz"]
                for fegyver in fightFegyverek:
                    commands.append(f"{fegyver.Nev} ({fegyver.Hasznalhato})")
                choice = curses.wrapper(menu, commands)
                for i in range(1,len(commands)):
                    if choice == commands[i]:
                        enemyHp = weaponChoose(fightFegyverek[i-1], enemy, enemyHp)
                        if fightFegyverek[i-1].Hasznalhato < 1:
                            elerhetoFegyverek.pop(i-1)
        elif choice == commands[2]:
            healthSystem()
    if jatekos.Hp <= 0:
        deathEnd()
    elif enemyHp <= 0:
        jatekos.Points += enemy.Points
        os.system("cls")
        text = [f"{enemy.Nev} meghalt. {enemy.Points} pontot kaptál legyőzéséért"]
        curses.wrapper(centertext, text, 5)
        text = [f"{enemy.Nev} meghalt. {enemy.Points} pontot kaptál legyőzéséért", f"Jelenlegi pontszámod: {jatekos.Points}"]
        curses.wrapper(centertext, text, 5)
        # #var(6)
        os.system("cls")

def weaponChoose(fegyver, enemy, enemyHp):
    if fegyver.Hasznalhato != 0:
        enemyHp -= fegyver.Dmg
        if enemyHp >= 0:
            text = [f"Az ellenség {fegyver.Dmg} sebzést szenvedett. Jelenlegi életereje: {enemyHp}"]
            curses.wrapper(centertext, text, 5)
            # #var(6)
            os.system("cls")
        else:
            text = [f"Az ellenség {fegyver.Dmg} sebzést szenvedett. Jelenlegi életereje: 0"]
            curses.wrapper(centertext, text, 5)
            # var(6)
            os.system("cls")
        fegyver.Hasznalhato -= 1
        if enemyHp > 0:
            text = ["Az ellenség visszatámad."]
            curses.wrapper(centertext, text, 5)
            # var(6)
            os.system("cls")
            jatekos.Hp -= enemy.Dmg
            if jatekos.Hp >= 0:
                text = [f"{enemy.Dmg} sebzést szenvedtél. Jelenlegi életerőd: {jatekos.Hp}"]
                curses.wrapper(centertext, text, 5)
                # var(6)
                os.system("cls")
            else:
                text = [f"{enemy.Dmg} sebzést szenvedtél. Jelenlegi életerőd: 0"]
                curses.wrapper(centertext, text, 5)
                # var(6)
                os.system("cls")
    else:
        text = [f"Sajnos a {fegyver.Nev} ebben a harcban már nem használható."]
        curses.wrapper(centertext, text, 5)
        # var(6)
        os.system("cls")
    return enemyHp

def handFight(enemyHp, enemy):
    text = ["Mivel nincsen fegyvered kézzel harcolsz."]
    curses.wrapper(centertext, text, 5)
    # var(6)
    os.system("cls")
    enemyHp -= jatekos.Dmg
    if enemyHp >= 0:
        text = [f"Az ellenség {jatekos.Dmg} sebzést szenvedett. Jelenlegi életereje: {enemyHp}"]
        # var(6)
        curses.wrapper(centertext, text, 5)
        os.system("cls")
    else:
        text = [f"Az ellenség {jatekos.Dmg} sebzést szenvedett. Jelenlegi életereje: 0"]
        # var(6)
        curses.wrapper(centertext, text, 5)
        os.system("cls")
    if enemyHp > 0:
        text = ["Az ellenség visszatámad."]
        var(6)
        curses.wrapper(centertext, text, 5)
        os.system("cls")
        jatekos.Hp -= enemy.Dmg
        if jatekos.Hp >= 0:
            text = [f"{enemy.Dmg} sebzést szenvedtél. Jelenlegi életerőd: {jatekos.Hp}"]
            curses.wrapper(centertext, text, 5)
            # var(6)
            os.system("cls")
        else:
            text = [f"{enemy.Dmg} sebzést szenvedtél. Jelenlegi életerőd: 0"]
            curses.wrapper(centertext, text, 5)
            #var(6)
            os.system("cls")
            deathEnd()
    return enemyHp

def healthSystem():
    global elerhetoHealek
    healErtek = 30
    if elerhetoHealek == 0:
        text = ["Sajnos nincsen elérhető életerő növelőd."]
        curses.wrapper(centertext, text, 5)
        #var(6)
        os.system("cls")
    elif jatekos.Hp == 100:
        text = ["Nincsen szükséged életerő növelésre."]
        curses.wrapper(centertext, text, 5)
        #var(6)
        os.system("cls")
    else:
        if jatekos.Hp + healErtek > 100:
            hozzaadandoHp = 100 - jatekos.Hp
            jatekos.Hp += hozzaadandoHp
        else:
            jatekos.Hp += healErtek
        text = ["Életerő feltöltve."]    
        curses.wrapper(centertext, text, 5)
        text = ["Életerő feltöltve.", f"Jelenlegi életerő: {jatekos.Hp}"] 
        curses.wrapper(centertext, text, 5) 
        #var(6)
        os.system("cls")
        elerhetoHealek -= 1

def healthBuy():
    global elerhetoHealek
    text = ["500 pont - 1 életerő növelő"]
    curses.wrapper(centertext, text, 5)
    text = ["500 pont - 1 életerő növelő", f"Pontjaid: {jatekos.Points}"]
    curses.wrapper(centertext, text, 5)
    #var(6)
    os.system("cls")
    commands = ["Vásárolsz életerő növelőt?", "Igen", "Nem"]
    choice = curses.wrapper(menu, commands)
    if choice == commands[1]:
        if jatekos.Points - 500 < 0:
            text = ["Nincsen elegendő pontod."]
            curses.wrapper(centertext, text, 5)
            #var(6)
            os.system("cls")
            healthBuy()
        else:
            jatekos.Points -= 500
            elerhetoHealek += 1
            text = [f"Életerő növelők száma eggyel megnövelve. Jelenlegi mennyiség: {elerhetoHealek} darab"]
            curses.wrapper(centertext, text, 5)
            #var(6)
            os.system("cls")
            if jatekos.Points >= 500:
                healthBuy()

def room1():
    global szobaid, elerhetoHealek
    szobaid = 1
    save()
    commands = ["Nagy szemeteskukák között vagy.", "Körülnézek", "Visszasétálok"]
    choice = curses.wrapper(menu, commands)
    if choice == commands[1]:
        if roomFirst[szobaid]:
            roomFirst[szobaid] = False
            text = ["Két kuka között észreveszel egy alkoholos üveget, az alján még pár cseppel."]
            curses.wrapper(centertext, text)
            # #var(5)
            text = ["Két kuka között észreveszel egy alkoholos üveget, az alján még pár cseppel.","Nem sokkal arrébb találsz néhány anyagdarabot is."]
            curses.wrapper(centertext, text)
            # #var(5)
            os.system("cls")
            elerhetoHealek += 2
            text = [f"Gratulálok, ezennel feloldottad az életerő növelőket. Jelenlegi mennyiség: {elerhetoHealek} darab"]
            curses.wrapper(centertext, text)
            #var(5)
            os.system("cls")
        else:
            text = ["A kukák között már mindent megtaláltál."]
            curses.wrapper(centertext, text)
            #var(5)
            os.system("cls")
    startRoom()

def room2():
    global szobaid
    szobaid = 2
    save()
    commands = ["Egy park közepén találtad magad.", "Elmegyek az épületek felé", "Elmegyek a bolt felé", "Visszamegyek", "Körülnézek"]
    choice = curses.wrapper(menu, commands)
    os.system("cls")
    if choice == commands[1]:
        room4()
    elif choice == commands[2]:
        room5()
    elif choice == commands[3]:
        startRoom()
    elif choice == commands[4]:
        os.system("cls")
        text = ["A város parkját kutatva egy táblára leszel figyelmes ami a városrész térképét mutatja."]
        curses.wrapper(centertext, text)
        os.system("cls")
        text = ["__________   _________   _________","|          | |         | |         |","| Szemetes |-|Városkapu|-| Sikátor |","|__________| |_________| |_________|"," |","__________   _________   _________","|          | |         | |         |","|   Bolt   |-|  Park   |-|Csatorna |","|__________| |_________| |_________|"]
        curses.wrapper(centertext, text, 99) 
        os.system("cls")
        room2()
def room3():
    global szobaid
    szobaid = 3
    save()
    commands = ["Egy sikátorba érkezel, ahol furcsa hangokat hallasz.", "Körbenézek", "Visszafutok"]
    choice = curses.wrapper(menu, commands)
    if choice == commands[1]:
        if fegyverek[2] not in elerhetoFegyverek:
            os.system("cls")
            kiir("szovegek/3")
            elerhetoFegyverek.append(fegyverek[2])
            text = [f"Gratulálok, ezennel feloldottad a következő fegyvert: {fegyverek[2].Nev} (Használhatóság: {fegyverek[2].Hasznalhato}, Sebzés: {fegyverek[2].Dmg})"]
            curses.wrapper(centertext, text, 5)
            os.system("cls")
        else:
            text = [f"Mivel nem találsz semmit visszatérsz a kapuhoz."]
            curses.wrapper(centertext, text, 5)
            os.system("cls")
    startRoom()

def room4(): #lehetne itt heal
    global szobaid
    szobaid = 4
    save()
    if roomFirst[szobaid]:
        roomFirst[szobaid] = False
        kiir("szovegek/4")
        fightSystem(opponents[1])
        text =["Ezt szerencsére megúsztad..."]
        curses.wrapper(centertext, text, 5)
        # #var(76)
        os.system("cls")
    else:
        text = ["Inkább úgy döntesz nem mész vissza, hisz nem találtál ott semmit..."]
        curses.wrapper(centertext, text, 5)
        #var(76)
        os.system("cls")
    room2()

def room5():
    global szobaid
    szobaid = 5
    save()
    text = ["Amint belépsz a boltba, egy hullával találod szemben magad."]
    curses.wrapper(centertext, text, 5)
    #var(76)
    text = ["Épphogy magadhoz térsz, egy sötét alakot veszel észre a sarokban."]
    curses.wrapper(centertext, text, 5, ["red"])
    #var(76)
    text = ["Másodpercekkel később már a földön vagy, rajtad pedig egy megvadult ember szerű lény."]
    curses.wrapper(centertext, text, 5, ["cya"])
    #var(76)
    os.system("cls")
    jatekos.Hp -= 5
    text = [f"5 sebzést szenvedtél. Jelenlegi életerőd: {jatekos.Hp} HP"]
    curses.wrapper(centertext, text, 5)
    #var(76)
    os.system("cls")
    if jatekos.Hp > 0:
        text = ["Lerúgod magadról majd elkezdesz a falon található lyuk felé futni."]
        curses.wrapper(centertext, text, 5)
        #var(76)
        os.system("cls")
        room6()
    else:
        deathEnd()

def room6():
    global szobaid
    szobaid = 6
    text = ["Szerencsére sikerül elmenekülnöd a lyukon keresztül,"]
    curses.wrapper(centertext, text, 5, ["mag"])
    #var(76)
    text = ["Szerencsére sikerül elmenekülnöd a lyukon keresztül,","ám a befelé vezető utat már egy eldőlt szekrény torlaszolja el."]
    curses.wrapper(centertext, text, 5)
    #var(76)
    os.system("cls")
    commands = ["Körülnézve látod, hogy a bolt raktárában vagy.", "Körülnézek", "Menekülök tovább"]
    choice = curses.wrapper(menu, commands)
    if choice == commands[1]:
        text = ["Kutakodás közben az egyik polc alatt észreveszel valamit. Kihúzod és jobban megnézed."]
        curses.wrapper(centertext, text, 5)
        #var(75)
        os.system("cls")
        elerhetoFegyverek.append(fegyverek[1])
        text = [f"Gratulálok, ezennel feloldottad a következő fegyvert: {fegyverek[1].Nev} (Használhatóság: Végtelen, Sebzés: {fegyverek[1].Dmg})"]
        curses.wrapper(centertext, text, 5)
        #var(75)
        os.system("cls")
        text = ["Keresgélsz még de nem találsz semmi mást, így továbbmész."]
        curses.wrapper(centertext, text, 5)
        #var(75)
        os.system("cls")
    room7()

def room7():
    global szobaid
    szobaid = 7
    save()
    text = ["Ismét az utcákon találod magad."]
    curses.wrapper(centertext, text, 5)
    #var(74)
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
    text = ["A családi ház előterébe lépsz."]
    curses.wrapper(centertext, text, 5)
    #var(74)
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
    if roomFirst[szobaid]:
        roomFirst[szobaid] = False
        kiir("szovegek/9")
        commands = ["Hozol gyógyszert a kisfiúnak?", "Igen", "Nem"]
        choice = curses.wrapper(menu, commands)
        if choice == commands[1]:
            text = [f"Köszönöm...A neved?"]
            curses.wrapper(centertext, text, 5, ["cya"])
            #var(75)
            text = [f"Köszönöm...A neved?","Megmondod a neved."]
            #var(75)
            curses.wrapper(centertext, text, 5, ["cya", ""])
            text = [f"Köszönöm...A neved?","Megmondod a neved.",f"Köszönöm {jatekos.Nev}!"]
            curses.wrapper(centertext, text, 5, ["cya", "", "cya"])
            #var(75)
            text = [f"Köszönöm...A neved?","Megmondod a neved.",f"Köszönöm {jatekos.Nev}!","Elindulsz gyógyszert keresni."]
            curses.wrapper(centertext, text, 5, ["cya", "", "cya", ""])
            #var(75)
            os.system("cls")
        else:
            quests["segitseg"] = False
            text = ["Sajnálom..nem tehetek mást...Sajnálom!!"]
            curses.wrapper(centertext, text, 5, ["red"])
            #var(75)
            text = ["Sajnálom..nem tehetek mást...Sajnálom!!","Az édesapa egyszer csak rádtámad."]
            curses.wrapper(centertext, text, 5, ["red", ""])
            #var(75)
            os.system("cls")
            fightSystem(opponents[5])
            kiir("szovegek/9.1")
            os.system("cls")
    else:
        if quests["segitseg"]:
            if quests["gyogyszer"] == False:
                text = [f"A gyógyszer...?"]
                curses.wrapper(centertext, text, 5, ["cya"])
                #var(75)
                os.system("cls")
            else:
                if fegyverek[3] not in elerhetoFegyverek:
                    jatekos.Points += 5000
                    text = [f"Visszajöttél...A gyógyszer?"]
                    curses.wrapper(centertext, text, 5, ["cya"])
                    #var(75)
                    text = ["Visszajöttél...A gyógyszer?", "Odanyújtod neki."]
                    curses.wrapper(centertext, text, 5, ["cya", ""])
                    #var(75)
                    text = ["Visszajöttél...A gyógyszer?", "Odanyújtod neki.",f"Köszönöm...cserébe tedd el ezt."]
                    curses.wrapper(centertext, text, 5, ["cya", "", "cya"])
                    #var(75)
                    text = ["Visszajöttél...A gyógyszer?", "Odanyújtod neki.",f"Köszönöm...cserébe tedd el ezt.","Egy fegyvert és egy kulcsot nyújt feléd."]
                    curses.wrapper(centertext, text, 5, ["cya", "", "cya", ""])
                    #var(75)
                    os.system("cls")
                    elerhetoFegyverek.append(fegyverek[3])
                    quests["varosKulcs"] = True
                    text = [f"Gratulálok, ezennel feloldottad a következő fegyvert: {fegyverek[3].Nev} (Használhatóság: {fegyverek[3].Hasznalhato}, Sebzés: {fegyverek[3].Dmg})"]
                    curses.wrapper(centertext, text, 5)
                    #var(75)
                    os.system("cls")
                    text = ["Elteszed a kulcsot is, bár nem tudod mit nyithat..."]
                    curses.wrapper(centertext, text, 5)
                    #var(75)
                    os.system("cls")
                else:
                    text = ["Inkább nem zaklatod őket..."]
                    curses.wrapper(centertext, text, 5)
                    #var(75)
                    os.system("cls")
        else:
            text = ["Nem vagy képes visszatérni az emeletre..."]
            curses.wrapper(centertext, text, 5)
            #var(75)
            os.system("cls")
    room8()

def room10():
    global szobaid
    szobaid = 10
    save()
    if roomFirst[szobaid]:
        roomFirst[szobaid] = False
        text = ["A családi ház pincéjében találod magad."]
        curses.wrapper(centertext, text, 5)
        #var(75)
        text = ["A családi ház pincéjében találod magad.", "Éppen elkezdenél körülnézni, mikor egy zombi fut feléd teljes sebességgel."]
        curses.wrapper(centertext, text, 5, ["", ""])
        #var(75)
        os.system("cls")
        fightSystem(opponents[2])
        text = ["Ahogy a holttest fölött állsz, csak remélheted, hogy a nő nem a ház lakosa volt egykor..."]
        curses.wrapper(centertext, text, 5)
        #var(75)
        text = ["Ahogy a holttest fölött állsz, csak remélheted, hogy a nő nem a ház lakosa volt egykor...","Éppen távozni készülsz, mikor észreveszel valamit az egyik sarokban."]
        curses.wrapper(centertext, text, 5)
        #var(75)
        os.system("cls")
        elerhetoFegyverek.append(fegyverek[4])
        text = [f"Gratulálok, ezennel feloldottad a következő fegyvert: {fegyverek[4].Nev} (Használhatóság: {fegyverek[4].Hasznalhato}, Sebzés: {fegyverek[4].Dmg})"]
        curses.wrapper(centertext, text, 5)
        #var(75)
        os.system("cls")
    else:
        text = ["A pincében már mindent felkutattál."]
        curses.wrapper(centertext, text, 5)
        #var(75)
        os.system("cls")
    room8()

def room11():
    global szobaid
    szobaid = 11
    save()
    text = ["Az ajtón átlépve egy gyógyszertárba érkezel"]
    curses.wrapper(centertext, text, 5)
    #var(75)
    os.system("cls")
    commands = ["Itt biztosan találni gyógyszereket...", "Gyógyszert keresek", "Életerő növelőt veszek", "Továbbmegyek egyenesen", "Visszamegyek"]
    choice = curses.wrapper(menu, commands)
    if choice == commands[1]:
        if quests["gyogyszer"] == False:
            quests["gyogyszer"] = True
            text = ["A pultok mögött körülnézve többféle gyógyszert is találsz."]
            curses.wrapper(centertext, text, 5)
            #var(75)
            text = ["A pultok mögött körülnézve többféle gyógyszert is találsz.","Mindet elhozod, hiszen jól jöhet."]
            curses.wrapper(centertext, text, 5)
            #var(75)
            os.system("cls")
        else:
            text = ["Már az összes gyógyszert összeszedted."]
            curses.wrapper(centertext, text, 5)
            #var(75)
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
    text = ["Kilépsz, és a gyógyszertár hátsó lerakóhelyénél találod magad."]
    curses.wrapper(centertext, text, 5)
    #var(75)
    os.system("cls")
    commands = ["Pár méterre egy 10 emeletes hátsó bejáratát látod.", "Bemegyek", "Körülnézek"]
    choice = curses.wrapper(menu, commands)
    if choice == commands[1]:
        text = ["Éppen elindulsz az ajtó felé, mikor mögötted megjelenik egy horda zombi."]
        curses.wrapper(centertext, text, 5)
        #var(75)
        text = ["Éppen elindulsz az ajtó felé, mikor mögötted megjelenik egy horda zombi.","Elkezdesz rohanni."]
        curses.wrapper(centertext, text, 5)
        #var(75)
        text = ["Éppen elindulsz az ajtó felé, mikor mögötted megjelenik egy horda zombi.","Elkezdesz rohanni.","Épphogy belépsz az ajtón, a zombik nagy lendülettel rohannak neki,","ezzel a visszautat elzárva."]
        #var(75)
        curses.wrapper(centertext, text, 5)
        #var(75)
        os.system("cls")
        room13()
    else:
        text = ["Ahogy kutatsz, észreveszel valamit az egyik ott álló kamion alatt..."]
        curses.wrapper(centertext, text, 5)
        #var(75)
        os.system("cls")
        elerhetoFegyverek.append(fegyverek[5])
        text = [f"Gratulálok, ezennel feloldottad a következő fegyvert: {fegyverek[5].Nev} (Használhatóság: {fegyverek[5].Hasznalhato}, Sebzés: {fegyverek[5].Dmg})"]
        curses.wrapper(centertext, text, 5)
        #var(75)
        os.system("cls")
        text = ["Éppen indulnál tovább, mikor egy zombihorda rohan feléd teljes sebességel."]
        curses.wrapper(centertext, text, 5)
        #var(75)var(
        text = ["Éppen indulnál tovább, mikor egy zombihorda rohan feléd teljes sebességel.","Elkezdesz rohanni, de mielőtt a házhoz érnél elkapják a lábad."]
        curses.wrapper(centertext, text, 5)
        #var(75)
        jatekos.Hp -= 10
        text = ["Éppen indulnál tovább, mikor egy zombihorda rohan feléd teljes sebességel.","Elkezdesz rohanni, de mielőtt a házhoz érnél elkapják a lábad.",f"10 sebzést szenvedtél. Jelenlegi életerőd: {jatekos.Hp} HP"]
        #var(75)
        curses.wrapper(centertext, text, 5)
        if jatekos.Hp <= 0:
            deathEnd()
        else:
            #var(75)
            text = ["Éppen indulnál tovább, mikor egy zombihorda rohan feléd teljes sebességel.","Elkezdesz rohanni, de mielőtt a házhoz érnél elkapják a lábad.",f"10 sebzést szenvedtél. Jelenlegi életerőd: {jatekos.Hp} HP","Szerencsére sikerül elérned az ajtóig, ám azt az annak rohanó zombik torlaszolják el,","ezzel eltorlaszolva a visszautat."]
            #var(75)
            curses.wrapper(centertext, text, 8)
            os.system("cls")
            room13()

def room13():
    global szobaid
    szobaid = 13
    save()
    if roomFirst[szobaid]:
        roomFirst[szobaid] = False
        text = ["Az épületbe lépve sokkos állapotodban elkezdesz kopogni a legközelebbi ajtón."]
        curses.wrapper(centertext, text, 5)
        #var(75)
        text = ["Az épületbe lépve sokkos állapotodban elkezdesz kopogni a legközelebbi ajtón.","Egy idős férfi nyit ajtót...","fegyvert fogva rád."]
        #var(75)
        curses.wrapper(centertext, text, 5)
        #var(75)
        os.system("cls")
        text = [f"Mekkora szerencse, hogy pont megjelentél..."]
        curses.wrapper(centertext, text, 5,["gre"])
        #var(75)
        text = ["Mekkora szerencse, hogy pont megjelentél...",f"Lenne egy kérésem hozzád, bár nem éppen vagy abban a helyzetben, hogy visszautasítsd."]
        curses.wrapper(centertext, text, 5,["gre"])
        #var(75)
        text = ["Mekkora szerencse, hogy pont megjelentél...",f"Lenne egy kérésem hozzád, bár nem éppen vagy abban a helyzetben, hogy visszautasítsd.","Hozd le nekem a két unokámat a 2. emeletről."]
        #var(75)
        curses.wrapper(centertext, text, 5,["gre"])
        text = ["Mekkora szerencse, hogy pont megjelentél...",f"Lenne egy kérésem hozzád, bár nem éppen vagy abban a helyzetben, hogy visszautasítsd.","Hozd le nekem a két unokámat a 2. emeletről.",f'"Az emeleten van egy férfi, de valahogy úgyis megoldod..."']
        #var(75)
        curses.wrapper(centertext, text, 5,["gre","gre","gre","gre",""])
        text = ["Mekkora szerencse, hogy pont megjelentél...",f"Lenne egy kérésem hozzád, bár nem éppen vagy abban a helyzetben, hogy visszautasítsd.","Hozd le nekem a két unokámat a 2. emeletről.",f'"Az emeleten van egy férfi, de valahogy úgyis megoldod..."',"Nincsen más lehetőséged, így elindulsz az épület folyosójára."]
        #var(75)
        curses.wrapper(centertext, text, 5,["gre"])
        os.system("cls")
    else:
        if quests["gyerekek"]:
            if quests["epuletKulcs"]:
                text = ["Inkább nem mész vissza..."]
                curses.wrapper(centertext, text, 5)
                #var(75)
                os.system("cls")
            else:
                text = [f'"Látom elhoztad nekem őket, köszönöm..."']
                curses.wrapper(centertext, text, 5,["gre"])
                #var(75)
                text = ["Látom elhoztad nekem őket, köszönöm...",f'"Most vedd el ezt és tűnj el innen!"']
                curses.wrapper(centertext, text, 5,["gre"])
                os.system("cls")
                #var(75)
                quests["epuletKulcs"] = True
                text = ["A kezedbe nyomott egy kulcsot..."]
                curses.wrapper(centertext, text, 5)
                #var(75)
                text = ["A kezedbe nyomott egy kulcsot...", "Ezzel ki tudsz jutni..."]
                curses.wrapper(centertext, text, 5)
                #var(75)
                os.system("cls")
        else:
            text = ["A gyerekek nélkül nem mersz visszatérni..."]
            curses.wrapper(centertext, text, 5)
            #var(75)
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
            text = ["Zárva..."]
            curses.wrapper(centertext, text, 5)
            #var(75)
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
        if roomFirst[szobaid]:
            roomFirst[szobaid] = False
            text = ["Leskelődés közben észreveszel a földön egy falról leesett elsősegély dobozt."]
            curses.wrapper(centertext, text, 5)
            #var(75)
            os.system("cls")
            elerhetoHealek += 1
            text = [f"Gratulálok, találtál egy életerő növelőt. Jelenlegi mennyiség: {elerhetoHealek} darab"]
            curses.wrapper(centertext, text, 5)
            #var(75)
            os.system("cls")
            room15()
        else:
            text = ["Már mindent megtaláltál ezen az emeleten."]
            curses.wrapper(centertext, text, 5)
            #var(75)
            os.system("cls")
            room15()
    elif choice == commands[2]:
        room16()
    else:
        room14()

def room16():
    global szobaid
    szobaid = 16
    if roomFirst[szobaid]:
        roomFirst[szobaid] = False
        text = ["A második emeletre érsz."]
        curses.wrapper(centertext, text, 5)
        #var(75)
        text = ["A második emeletre érsz.","Amint fellépsz az utolsó lépcsőfokon, már érted kiről beszélt az idős férfi..."]
        curses.wrapper(centertext, text, 5)
        #var(75)
        text = ["A második emeletre érsz.","Amint fellépsz az utolsó lépcsőfokon, már érted kiről beszélt az idős férfi...", "Egy bandita lő rád fegyverével, de szerencsére nem talál el..."]
        #var(75)
        curses.wrapper(centertext, text, 5)
        os.system("cls")
        fightSystem(opponents[3])
        text = ["El sem hiszed, hogy sikerült túlélned."]
        curses.wrapper(centertext, text, 5)
        #var(75)
        text = ["El sem hiszed, hogy sikerült túlélned.","Szörnyen érzed magad amiatt amit tettél, de tudod,","hogy az életed múlt rajta..."]
        #var(75)
        curses.wrapper(centertext, text, 5)
        #var(75)
        text = ["El sem hiszed, hogy sikerült túlélned.","Szörnyen érzed magad amiatt amit tettél, de tudod,","hogy az életed múlt rajta...","Kicsit megnyugszol, majd belépsz a lakásba, ahol a gyerekek vannak."]
        #var(75)
        curses.wrapper(centertext, text, 5)
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
    text = ["A lakásba lépve meglátod a két kisgyereket."]
    curses.wrapper(centertext, text, 5)
    #var(75)
    text = ["A lakásba lépve meglátod a két kisgyereket.","Egy 6 év körülinek tűnő kisfiú és a nővére áll veled szemben,","félelemmel a szemükben."]
    curses.wrapper(centertext, text, 5)
    #var(75)
    #var(75)
    text = ["A lakásba lépve meglátod a két kisgyereket.","Egy 6 év körülinek tűnő kisfiú és a nővére áll veled szemben,","félelemmel a szemükben.","Elmagyarázod nekik, hogy ki vagy és miért jöttél."]
    #var(75)
    curses.wrapper(centertext, text, 5)
    text = ["A lakásba lépve meglátod a két kisgyereket.","Egy 6 év körülinek tűnő kisfiú és a nővére áll veled szemben,","félelemmel a szemükben.","Elmagyarázod nekik, hogy ki vagy és miért jöttél.","A magyarázat hallatán közelebb lépnek hozzád."]
    #var(75)
    curses.wrapper(centertext, text, 5)
    text = ["A lakásba lépve meglátod a két kisgyereket.","Egy 6 év körülinek tűnő kisfiú és a nővére áll veled szemben,","félelemmel a szemükben.","Elmagyarázod nekik, hogy ki vagy és miért jöttél.","A magyarázat hallatán közelebb lépnek hozzád.",f"Köszönjük szépen..."]
    #var(75)
    szinek = ["","","","","","cya"]
    curses.wrapper(centertext, text, 5, szinek)
    text = ["A lakásba lépve meglátod a két kisgyereket.","Egy 6 év körülinek tűnő kisfiú és a nővére áll veled szemben,","félelemmel a szemükben.","Elmagyarázod nekik, hogy ki vagy és miért jöttél.","A magyarázat hallatán közelebb lépnek hozzád.",f"Köszönjük szépen...","Látszólag készen állnak követni téged."]
    szinek = ["","","","","","cya",""]
    curses.wrapper(centertext, text, 5, szinek)
    #var(75)
    os.system("cls")
    room16()

def room18():
    global szobaid
    szobaid = 18
    save()
    if roomFirst[szobaid]:
        roomFirst[szobaid] = False
        text = ["Felérve a harmadik emeletre mozgásra leszel figyelmes..."]
        curses.wrapper(centertext, text, 5)
        #var(75)
        text = ["Felérve a harmadik emeletre mozgásra leszel figyelmes...","Ekkor veszed észre a sarokban ülő, fertőzött lakót."]
        curses.wrapper(centertext, text, 5)
        #var(75)
        text = ["Felérve a harmadik emeletre mozgásra leszel figyelmes...","Ekkor veszed észre a sarokban ülő, fertőzött lakót.","Amint észrevesz téged rádtámad."]
        #var(75)
        curses.wrapper(centertext, text, 5)
        os.system("cls")
        fightSystem(opponents[2])
        text = ["Szerencsére sikerült megölnöd..."]
        curses.wrapper(centertext, text, 5)
        #var(75)
        os.system("cls")
        commands = ["A lépcső a negyedik emeletre le van szakadva.", "Körülnézek", "Lemegyek"]
        choice = curses.wrapper(menu, commands)
        if choice == commands[1]:
            if fegyverek[6] not in elerhetoFegyverek:
                text = ["A lépcső romjai között figyelmes leszel valamire."]
                #var(75)
                os.system("cls")
                elerhetoFegyverek.append(fegyverek[6])
                text = [f"Gratulálok, ezennel feloldottad a következő fegyvert: {fegyverek[6].Nev} (Használhatóság: {fegyverek[6].Hasznalhato}, Sebzés: {fegyverek[6].Dmg})"]
                curses.wrapper(centertext, text, 5)
                #var(75)
                os.system("cls")
                room18()
            else:
                text = ["Mindent megtaláltál már."]
                curses.wrapper(centertext, text, 5)
                #var(75)
                os.system("cls")
                room18()
        else:
            room16()
    else:
        commands = ["A lépcső a negyedik emeletre le van szakadva.", "Körülnézek", "Lemegyek"]
        choice = curses.wrapper(menu, commands)
        if choice == commands[1]:
            if fegyverek[6] not in elerhetoFegyverek:
                text = ["A lépcső romjai között figyelmes leszel valamire."]
                curses.wrapper(centertext, text, 5)
                #var(75)
                os.system("cls")
                elerhetoFegyverek.append(fegyverek[6])
                text = [f"Gratulálok, ezennel feloldottad a következő fegyvert: {fegyverek[6].Nev} (Használhatóság: {fegyverek[6].Hasznalhato}, Sebzés: {fegyverek[6].Dmg})"]
                curses.wrapper(centertext, text, 5)
                #var(75)
                os.system("cls")
                room18()
            else:
                text = ["Mindent megtaláltál már."]
                curses.wrapper(centertext, text, 5)
                #var(75)
                os.system("cls")
                room18()
        else:
            room16()

def room19():
    global szobaid
    szobaid = 19
    save()
    commands = ["A ház melletti utcára lépsz ki.", "Körülnézek", "Megnézem a kaput", "Elmegyek balra"]
    choice = curses.wrapper(menu, commands)
    if choice == commands[1]:
        if fegyverek[7] not in elerhetoFegyverek:
            text = ["A dobozok között nézelődve egyszercsak szuszogásra leszel figyelmes."]
            curses.wrapper(centertext, text, 5)
            #var(75)
            text = ["A dobozok között nézelődve egyszercsak szuszogásra leszel figyelmes.","Közelebb lépve egy juhászkutyát találsz összekuporodva az egyik dobozban."]
            curses.wrapper(centertext, text, 5)
            #var(75)
            os.system("cls")
            elerhetoFegyverek.append(fegyverek[7])
            text = ["Gratulálok, ezzennel a kutya a társad."]
            curses.wrapper(centertext, text, 5)
            #var(75)
            text = ["Gratulálok, ezzennel a kutya a társad.","Harcokban tudod őt használni, melyekben fegyverként működik."]
            curses.wrapper(centertext, text, 5)
            #var(75)
            text = ["Gratulálok, ezzennel a kutya a társad.","Harcokban tudod őt használni, melyekben fegyverként működik.",f"(Használhatóság: Végtelen, Sebzés: {fegyverek[7].Dmg})"]
            #var(75)
            curses.wrapper(centertext, text, 5)
            os.system("cls")
            room19()
        else:
            text = ["A dobozok környékén már mindent fontosat megtaláltál."]
            curses.wrapper(centertext, text, 5)
            #var(75)
            os.system("cls")
            room19()
    elif choice == commands[2]:
        if not quests["kapuKulcs"]:
            text = ["Az utca jobb oldalán egy kapu van."]
            curses.wrapper(centertext, text, 5)
            text = ["Az utca jobb oldalán egy kapu van.", "Megpróbálod kinyitni, de sajnos zárva van..."]
            curses.wrapper(centertext, text, 5)
        else:
            text = ["A kapu a kulccsal kinyílik."]
            curses.wrapper(centertext, text, 5)
            room20()
    else:
        room22()

def room20():
    global szobaid, elerhetoHealek
    szobaid = 20
    save()
    commands = ["A város főterén állsz, szemben egy óriási kapuval.", "Körülnézek", "Elmegyek a kapuhoz", "Elmegyek balra", "Visszamegyek"]
    choice = curses.wrapper(menu, commands)
    if choice == commands[1]:
        if roomFirst[szobaid]:
            roomFirst[szobaid] = False
            text = ["A padok között sétálva az egyiken észreveszel két elsősegély dobozt."]
            curses.wrapper(centertext, text, 5)
            #var(75)
            text = ["A padok között sétálva az egyiken észreveszel két elsősegély dobozt.","Habár nyitva vannak, néhány kötszer még található bennük."]
            curses.wrapper(centertext, text, 5)
            #var(75)
            os.system("cls")
            elerhetoHealek += 2
            text = ["A padok között sétálva az egyiken észreveszel két elsősegély dobozt.","Habár nyitva vannak, néhány kötszer még található bennük.",f"Gratulálok, találtál két életerő növelőt. Jelenlegi mennyiség: {elerhetoHealek} darab"]
            #var(75)
            curses.wrapper(centertext, text, 5)
            os.system("cls")
        else:
            text = ["Már mindent megtaláltál."]
            curses.wrapper(centertext, text, 5)
            #var(75)
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
    text = ["Ahogy közeledsz a kapuhoz, egyre inkább érzed,"]
    curses.wrapper(centertext, text, 5)
    #var(75)
    text = ["Ahogy közeledsz a kapuhoz, egyre inkább érzed,","hogy amiért eddig harcoltál végre itt van előtted."]
    curses.wrapper(centertext, text, 5)
    #var(75)
    text = ["Ahogy közeledsz a kapuhoz, egyre inkább érzed,","hogy amiért eddig harcoltál végre itt van előtted.","Ez a kapu jelenti a kijutásodat."]
    curses.wrapper(centertext, text, 5)
    #var(75)
    os.system("cls")
    text = ["A kapu előtt állsz, készen arra, hogy elhagyd ezt a helyet..."]
    #var(75)
    curses.wrapper(centertext, text, 5)
    text = ["A kapu előtt állsz, készen arra, hogy elhagyd ezt a helyet...","...ám ekkor érdekes hangot hallassz magad mögül."]
    curses.wrapper(centertext, text, 5)
    #var(75)
    text = ["A kapu előtt állsz, készen arra, hogy elhagyd ezt a helyet...","...ám ekkor érdekes hangot hallassz magad mögül.","Hátrafordulva egy óriási mutáns zombit veszel észre."]
    #var(75)
    curses.wrapper(centertext, text, 5)
    text = ["A kapu előtt állsz, készen arra, hogy elhagyd ezt a helyet...","...ám ekkor érdekes hangot hallassz magad mögül.","Hátrafordulva egy óriási mutáns zombit veszel észre.","Mikor észrevesz ő is téged, teljes sebességel indul meg feléd."]
    #var(75)
    curses.wrapper(centertext, text, 5)
    os.system("cls")
    fightSystem(opponents[6])
    text = ["Sikerült megölnöd a zombit, ám a végkimerülés szélén állsz."]
    curses.wrapper(centertext, text, 5)
    #var(75)
    text = ["Sikerült megölnöd a zombit, ám a végkimerülés szélén állsz.","Ismét a kapu felé veszed az irányt."]
    #var(75)
    curses.wrapper(centertext, text, 5)
    os.system("cls")
    if quests["varosKulcs"] == False:
        if quests["letra"]:
            text = ["Ott állva veszed észre, hogy a kapu zárva,"]
            curses.wrapper(centertext, text, 5)
            #var(75)
            text = ["Ott állva veszed észre, hogy a kapu zárva,","az idős férfitől kapott kulcs pedig nem nyitja..."]
            #var(75)
            curses.wrapper(centertext, text, 5)
            text = ["Ott állva veszed észre, hogy a kapu zárva,","az idős férfitől kapott kulcs pedig nem nyitja...","Ekkor jut eszedbe a létra..."]
            #var(75)
            curses.wrapper(centertext, text, 5)
            text = ["Ott állva veszed észre, hogy a kapu zárva,","az idős férfitől kapott kulcs pedig nem nyitja...","Ekkor jut eszedbe a létra...","A sikátorban talált létrával sikerül átmásznod a kapun,"]
            #var(75)
            curses.wrapper(centertext, text, 5)
            text = ["Ott állva veszed észre, hogy a kapu zárva,","az idős férfitől kapott kulcs pedig nem nyitja...","Ekkor jut eszedbe a létra...","A sikátorban talált létrával sikerül átmásznod a kapun,","melynek a másik oldalán kimerülve érsz földet."]
            #var(75)
            curses.wrapper(centertext, text, 5)
            os.system("cls")
            gameEnd()
        else:
            text = ["Ott állva jössz rá, hogy a kiút zárva,"]
            curses.wrapper(centertext, text, 5)
            #var(75)
            text = ["Ott állva jössz rá, hogy a kiút zárva,","neked pedig nincsen kulcsod."]
            curses.wrapper(centertext, text, 5)
            #var(75)
            text = ["Ott állva jössz rá, hogy a kiút zárva,","neked pedig nincsen kulcsod.","Megpróbálsz átmászni, de a kapu túl magas..."]
            curses.wrapper(centertext, text, 5)
            #var(75)
            text = ["Ott állva jössz rá, hogy a kiút zárva,","neked pedig nincsen kulcsod.","Megpróbálsz átmászni, de a kapu túl magas...","Kimerülten esel a földre..."]
            curses.wrapper(centertext, text, 5)
            #var(75)
            text = ["Ott állva jössz rá, hogy a kiút zárva,","neked pedig nincsen kulcsod.","Megpróbálsz átmászni, de a kapu túl magas...","Kimerülten esel a földre...",f"Feladod..."]
            szinek = ["","","","","red"]
            curses.wrapper(centertext, text, 5, szinek)
            #var(75)
            os.system("cls")
            deathEnd()
    else:
        text = ["Ott állva veszed észre, hogy a kapu zárva."]
        curses.wrapper(centertext, text, 5)
        #var(75)
        text = ["Ott állva veszed észre, hogy a kapu zárva.","Kipróbálod az idős férfitől kapott kulcsot ám az nem nyitja..."]
        curses.wrapper(centertext, text, 5)
        #var(75)
        text = ["Ott állva veszed észre, hogy a kapu zárva.","Kipróbálod az idős férfitől kapott kulcsot ám az nem nyitja...","Ekkor jut eszedbe az apukától kapott kulcs."]
        #var(75)
        curses.wrapper(centertext, text, 5)
        text = ["Ott állva veszed észre, hogy a kapu zárva.","Kipróbálod az idős férfitől kapott kulcsot ám az nem nyitja...","Ekkor jut eszedbe az apukától kapott kulcs.","Belehelyezed a kulcslyukba és szerencsére kinyitja."]
        #var(75)
        curses.wrapper(centertext, text, 5)
        text = ["Ott állva veszed észre, hogy a kapu zárva.","Kipróbálod az idős férfitől kapott kulcsot ám az nem nyitja...","Ekkor jut eszedbe az apukától kapott kulcs.","Belehelyezed a kulcslyukba és szerencsére kinyitja.","Átlépsz a kapun és kimerülten esel a földre."]
        #var(75)
        curses.wrapper(centertext, text, 5)
        os.system("cls")
        gameEnd()

def room22():
    global szobaid
    szobaid = 22
    if roomFirst[szobaid]:
        roomFirst[szobaid] = False
        text = ["A szűk kis utcáról hirtelen egy főúton találod magad."]
        curses.wrapper(centertext, text, 5)
        text = ["A szűk kis utcáról hirtelen egy főúton találod magad.","A természet által visszafoglalt útban való gyönyörködésedet egy, a szemed sarkában felbukkanó furcsa árny töri meg."]
        curses.wrapper(centertext, text, 5)
        text = ["A szűk kis utcáról hirtelen egy főúton találod magad.","A természet által visszafoglalt útban való gyönyörködésedet egy, a szemed sarkában felbukkanó furcsa árny töri meg.", "Időd sincsen rájönni mi lehetett az,"]
        curses.wrapper(centertext, text, 5)
        text = ["A szűk kis utcáról hirtelen egy főúton találod magad.","A természet által visszafoglalt útban való gyönyörködésedet egy, a szemed sarkában felbukkanó furcsa árny töri meg.", "Időd sincsen rájönni mi lehetett az,", "mivel hirtelen egy éles fájdalmat érzel a fejedben és a világ elsötétül..."]
        curses.wrapper(centertext, text, 5)
        room23()
    else:
        pass

def room23():
    global szobaid
    szobaid = 23
    if roomFirst[szobaid]:
        roomFirst[szobaid] = False
        jatekos.Hp == 100
        kiir(23.1)
        text = [f'"Tehát {jatekos.Nev}..."']
        szin = ["cya"]
        curses.wrapper(centertext, text, 5, szin)
        text = [f'"Tehát {jatekos.Nev}..."', f'"És kedves {jatekos.Nev}, milyen céllal járod a várost?']
        szin = ["cya"]
        curses.wrapper(centertext, text, 5, szin)
        os.system("cls")
        kiir(23.2)

def room24():
    global szobaid
    szobaid = 24
    save()
    text = [f"'Szia {jatekos.nev}'"]
    curses.wrapper(centertext, text, 5, ["gre"])
    text = [f"'Szia {jatekos.nev}'", "'Jó napot, ismerjük egymást?'"]
    curses.wrapper(centertext, text, 5, ["gre",""])
    text = [f"'Szia {jatekos.nev}'", "'Jó napot, ismerjük egymást?'","'Elnézést még nem találkoztunk, Jánosnak hívnak'"]
    curses.wrapper(centertext, text, 5, ["gre","", ""])
    text = [f"'Szia {jatekos.nev}'", "'Jó napot, ismerjük egymást?'","'Elnézést még nem találkoztunk, Jánosnak hívnak'", "'Bázison az utóbbi időben másról sem beszélnek csak rólad"]
    curses.wrapper(centertext, text, 5, ["gre","", "gre", "gre"])
    text = [f"'Szia {jatekos.nev}'", "'Jó napot, ismerjük egymást?'","'Elnézést még nem találkoztunk, Jánosnak hívnak'", "'Bázison az utóbbi időben másról sem beszélnek csak rólad", "Mindenesetre, nálam tudsz pontokért fegyvert és életerő növelőt vásárolni"]
    curses.wrapper(centertext, text, 5, ["gre","", "gre", "gre", "gre"])
    healthBuy()

def room25():
    global szobaid
    szobaid = 25

def room26():
    global szobaid
    szobaid = 26
    if roomFirst[szobaid]:
        roomFirst[szobaid] = False
        kiir(26.1)
        fightSystem(opponents[2])
        kiir(26.2)

def room27():
    global szobaid
    szobaid = 27
    if roomFirst[szobaid]:
        roomFirst[szobaid] = False
        kiir(27)
        room28()

def room28():
    global szobaid
    szobaid = 28
    save()
    text = ["A boltba léptek."]
    curses.wrapper(centertext, text, 5)
    text = ["A boltba léptek.", "Az különböző konzervek külön-külön, szépen elrendezve állnak a polcokon."]
    curses.wrapper(centertext, text, 5)
    text = ["A boltba léptek.", "Az különböző konzervek külön-külön, szépen elrendezve állnak a polcokon.", "Biztosan rendszeresen járnak ide élelemért."]
    curses.wrapper(centertext, text, 5)
    os.system("cls")
    text = ['"Tudnál hozni mindegyik konzervből egyet?"']
    szin = ["cya"]
    curses.wrapper(centertext, text, 5, szin)
    text = ["Tudnál hozni mindegyik konzervből egyet?", f'"Köszönöm, hogy segítesz {jatekos.Nev}!"']
    szin = ["cya"]
    curses.wrapper(centertext, text, 5, szin)
    text = ["Tudnál hozni mindegyik konzervből egyet?", f'"Köszönöm, hogy segítesz {jatekos.Nev}!"', '"Induljunk vissza a bázisra."']
    szin = ["cya"]
    curses.wrapper(centertext, text, 5, szin)
    os.system("cls")
    text = ["A bázisra visszatérve néhány fiatal veszi át tőletek a konzerveket."]
    curses.wrapper(centertext, text, 5)
    os.system("cls")
    text = ['"Látom visszatértetek..."']
    szin = ["mag"]
    curses.wrapper(centertext, text, 5, szin)
    text = ['"Látom visszatértetek..."', '"Mostmár beszélhetünk az lényegről?"']
    szin = ["mag"]
    curses.wrapper(centertext, text, 5, szin)
    os.system("cls")
    text = [f'"{jatekos.Nev}, emlékszel az autóra a boltnál?"']
    curses.wrapper(centertext, text, 5, ["cya"])
    text = [f'"{jatekos.Nev}, emlékszel az autóra a boltnál?"', '"Szükségünk lenne rá..."']
    curses.wrapper(centertext, text, 5, ["cya"])
    text = [f'"{jatekos.Nev}, emlékszel az autóra a boltnál?"', '"Szükségünk lenne rá..."', '"Tudnál segíteni megszerezni?"']
    curses.wrapper(centertext, text, 5, ["cya"])
    os.system("cls")
    text = ['"Tudunk egy utat ki a városból, de kapuval van lezárva."']
    curses.wrapper(centertext, text, 5, ["cya"])
    text = ['"Tudunk egy utat ki a városból, de kapuval van lezárva."', '"A kulcsot hónapokig kerestük sikertelenül..."']
    curses.wrapper(centertext, text, 5, ["cya"])
    text = ['"Tudunk egy utat ki a városból, de kapuval van lezárva."', '"A kulcsot hónapokig kerestük sikertelenül..."','"Autóval viszont hamar áttudnánk törni rajtad,"']
    curses.wrapper(centertext, text, 5, ["cya"])
    text = ['"Tudunk egy utat ki a városból, de kapuval van lezárva."', '"A kulcsot hónapokig kerestük sikertelenül..."','"Autóval viszont hamar áttudnánk törni rajtad,"', '"Később aztán a többiekért is visszajönnénk."']
    curses.wrapper(centertext, text, 5, ["cya"])
    text = ['"Tudunk egy utat ki a városból, de kapuval van lezárva."', '"A kulcsot hónapokig kerestük sikertelenül..."','"Autóval viszont hamar áttudnánk törni rajtad,"', '"Később aztán a többiekért is visszajönnénk."', '"Ha segítesz, az elsők között lehetsz akik elhagyják a várost."']
    curses.wrapper(centertext, text, 5, ["cya"])
    text = ['"Tudunk egy utat ki a városból, de kapuval van lezárva."', '"A kulcsot hónapokig kerestük sikertelenül..."','"Autóval viszont hamar áttudnánk törni rajtad,"', '"Később aztán a többiekért is visszajönnénk."', '"Ha segítesz, az elsők között lehetsz akik elhagyják a várost."', '"Holnap reggel kéne elindulnok az ellenséges bázisra."']
    curses.wrapper(centertext, text, 5, ["cya"])
    text = ['"Tudunk egy utat ki a városból, de kapuval van lezárva."', '"A kulcsot hónapokig kerestük sikertelenül..."','"Autóval viszont hamar áttudnánk törni rajtad,"', '"Később aztán a többiekért is visszajönnénk."', '"Ha segítesz, az elsők között lehetsz akik elhagyják a várost."', '"Holnap reggel kéne elindulnok az ellenséges bázisra."', '"Ne aggódj, van időd dönteni reggelig."']
    curses.wrapper(centertext, text, 5, ["cya"])
    os.system("cls")
    text = ["Gergő sietve távozott a szobából."]
    curses.wrapper(centertext, text, 5)


def gameEnd():
    text = ["Sikerült kijutnod a városból..."]
    curses.wrapper(centertext, text, 5)
    #var(75)
    text = ["Sikerült kijutnod a városból...",f"de vajon mi vár a város falain kívül?"]
    curses.wrapper(centertext, text, 5, ["","red"])
    #var(5)
    os.system("cls")
    text = [f"JÁTÉK VÉGE\n"]
    curses.wrapper(centertext, text, 5, ["red"])
    #var(2)
    text = [f"JÁTÉK VÉGE\n",f"Elért pontszám: {jatekos.Points}"]
    curses.wrapper(centertext, text, 5, ["red",""])
    #var(2)
    text = [f"JÁTÉK VÉGE\n",f"Elért pontszám: {jatekos.Points}",f"Megszerzett fegyverek: {len(elerhetoFegyverek)}/{len(fegyverek)}"]
    curses.wrapper(centertext, text, 5, ["red","",""])
    #var(10)
    os.system("cls")
    endMenu()

def deathEnd():
    text = [f"MEGHALTÁL\n"]
    curses.wrapper(centertext, text, 5, ["red"])
    #var(2)
    text = [f"MEGHALTÁL\n",f"Elért pontszám: {jatekos.Points}"]
    curses.wrapper(centertext, text, 5, ["red",""])
    #var(2)
    text = [f"MEGHALTÁL\n",f"Elért pontszám: {jatekos.Points}",f"Megszerzett fegyverek: {len(elerhetoFegyverek)}/{len(fegyverek)}"]
    curses.wrapper(centertext, text, 5, ["red","",""])
    #var(10)
    os.system("cls")
    endMenu()

def endMenu():
    commands = ["Válassz az alábbiak közül", "Új játék", "Mentés betöltése", "Kilépés"]
    choice = curses.wrapper(menu, commands)
    if choice == commands[1]:
        gamestart()
    elif choice == commands[2]:
        load()
    else:
        exit()

def save():
    stri = ""
    f = open("save.txt", "w", encoding = "UTF-8")
    f.write(jatekos.Nev)
    f.write("\n")
    global jhp
    f.write(str(jatekos.Hp))
    f.write("\n")
    global szobaid
    f.write(str(szobaid))
    f.write("\n")
    global elerhetoFegyverek
    for i in elerhetoFegyverek:
        stri +=(str(i.Nev))+ ";"
    f.write(stri)
    f.write("\n")
    f.write(str(jatekos.Points))
    f.write("\n")
    f.write(str(elerhetoHealek))
    for keys, values in quests.items():
        f.write("\n")
        f.write(f"{str(keys)}:{str(values)}")
    for keys, values in roomFirst.items():
        f.write("\n")
        f.write(f"{str(keys)}:{str(values)}")

    f.close()

def load():
    f = open("save.txt", "r", encoding = "UTF-8")
    global jatekos
    jatekos = karakter
    jatekos.Nev = f.readline().strip()
    jatekos.Hp = int(f.readline().strip())
    global szobaid
    szobaid = f.readline().strip()
    global elerhetoFegyverek
    fegyvernevek = f.readline().strip().split(";")
    for nev in fegyvernevek:
        for fegyver in fegyverek:
            if fegyver.Nev == nev:
                elerhetoFegyverek.append(fegyver)
                break
    jatekos.Points = int(f.readline().strip())
    global elerhetoHealek
    elerhetoHealek = int(f.readline().strip())
    f.close()
    szobak = [startRoom,room1, room2, room3, room4, room5, room6, room7, room8, room9, room10, room11, room12, room13, room14, room15, room16, room17, room18, room19]
    szobak[int(szobaid)]()
    global quests
    for i in range(0,6):
        i = []
        i =  f.readline().strip().split(':')
        quests[i[0]] = i[1]
    global roomFirst
    for i in range(0,9):
        i = []
        i =  f.readline().strip().split(':')
        roomFirst[i[0]] = i[1]

    

def blackjack():
    cards = ['A', '2', '3','4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'a' ]
    pontoter= ['11', '2', '3','4', '5', '6', '7', '8', '9', '10','10','10','10', '1']
    kezen = []
    kerlapot = 0
    osszeg = 0
    for i in range(2):
        lap = random.randint(0,12)
        kezen.append(cards[lap])
        osszeg += int(pontoter[lap])
        if "A" in kezen and osszeg > 21:
            kezen = ["a" if x=="A" else x for x in kezen]
            osszeg -= 10
        elif osszeg > 21:
            print("Vesztettél")
            input("Nyomjon enter-t a kilépéshez\n")
            return
    print(kezen, osszeg)
    while kerlapot != "i" and kerlapot != "n":
        kerlapot = input("Kérsz még lapot? I/N ").lower()
    while kerlapot == "I" or kerlapot == "i":
        lap = random.randint(0,12)
        kezen.append(cards[lap])
        osszeg += int(pontoter[lap])
        if "A" in kezen and osszeg > 21:
            kezen = ["a" if x=="A" else x for x in kezen]
            osszeg -= 10
        elif osszeg > 21:
            print(kezen, osszeg)
            print("Vesztettél")
            input("Nyomjon enter-t a kilépéshez\n")
            return
        print(kezen, osszeg)
        kerlapot = input("Kérsz még lapot? I/N ")
    dealer = 0
    dealerkez = []
    while dealer < 21 and dealer <= osszeg:
        lap = random.randint(0,12)
        dealerkez.append(cards[lap])
        dealer += int(pontoter[lap])
        print(dealerkez, dealer)
    if "A" in kezen and osszeg > 21:
            kezen = ["a" if x=="A" else x for x in kezen]
            osszeg -= 10
    elif dealer > osszeg and dealer < 21:
        print("Vesztettél")
        input("Nyomjon enter-t a kilépéshez\n")
        return
    elif dealer > 21 and osszeg < 21: 
        print("Nyertél")
        input("Nyomjon enter-t a kilépéshez\n")
        return
    elif dealer == 21 and osszeg == 21:
        print("Döntetlen")
        input("Nyomjon enter-t a kilépéshez\n")
        return
