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
            return True
    return True


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
    commands = ["Kérlek állítsd be az ablak méretét","Folytatás"]
    global width
    choice = curses.wrapper(menu, commands)
    commands = ["Outback","Új játék", "Folytatás", "Kilépés"]
    width = os.get_terminal_size().columns
    choice = curses.wrapper(menu, commands)
    if choice == commands[1]:
        global roomFirst
        roomFirst = {1: True,4: True,9: True,10: True,13: True,15: True,16: True,18: True,20: True}
        global quests
        quests = {"gyogyszer": False,"segitseg": True,"gyerekek": False,"epuletKulcs": False,"varosKulcs": False,"letra": False}
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
    text = ["Az ehhez hasonló olvasnivalókat a 'SPACE' gomb megnyomásával tudod átlépni, de idővel automatikusan is átlép"]
    global width
    curses.wrapper(centertext, text, 999)
    text = [f"Nyomd meg az 'SPACE'-t a továbblépéshez és a tutorial elindításához"]
    curses.wrapper(centertext, text, 999)
    os.system("cls")
    text = [f"Egy szobában találtad magad egy robottal szemben"]
    curses.wrapper(centertext, text, 9)
    text = ["A hátizsákodban kutatva egy fegyvert találsz"]
    curses.wrapper(centertext, text, 9)
    text = ["A robot ellened fordul"]
    szin = ["red"]
    curses.wrapper(centertext, text, 9, szin)
    text = ["Az ilyen helyzetekben Outbackben egy menü fogad","itt tudsz életerőt regenerálni, fegyvert választani az enter lenyomásával"]
    szin = ["gre"]
    curses.wrapper(centertext, text, 9, szin)
    elerhetoFegyverek.append(fegyverek[0])
    os.system("cls")
    fightSystem(opponents[0])
    text = ["A harc közben jelentős mennyiségű életerőt vesztettél,","a játék során gyógyszertárakba is be tudsz térni ahol"," gyógyító tárgakat tudsz venni"]#bugos a szöveg
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
    while gamertag == "":
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
    for fegyver in elerhetoFegyverek:
        fightFegyverek.append(fegyver)
    enemyHp = enemy.Hp
    while jatekos.Hp > 0 and enemyHp > 0:
        commands = ["Kérlek válassz az alábbiak közül", "Támadás", "Gyógyítás"]
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
                            fightFegyverek.pop(i-1)
        elif choice == commands[2]:
            healthSystem()
    if jatekos.Hp <= 0:
        deathEnd()
    elif enemyHp <= 0:
        jatekos.Points += enemy.Points
        os.system("cls")
        text = [f"{enemy.Nev} meghalt. {enemy.Points} pontot kaptál legyőzéséért"]
        curses.wrapper(centertext, text, 5)
        text = [f"{enemy.Nev} meghalt. {enemy.Points} pontot kaptál legyőzéséért", f"Jelenlegi pontszámod:{jatekos.Points}"]
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
                text = [f"Sebzést szenvedtél. Jelenlegi életerőd: {jatekos.Hp}"]
                curses.wrapper(centertext, text, 5)
                # var(6)
                os.system("cls")
            else:
                text = ["Sebzést szenvedtél. Jelenlegi életerőd: 0"]
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
            text = [f"Sebzést szenvedtél. Jelenlegi életerőd: {jatekos.Hp}"]
            curses.wrapper(centertext, text, 5)
            # var(6)
            os.system("cls")
        else:
            text = ["Sebzést szenvedtél. Jelenlegi életerőd: 0"]
            curses.wrapper(centertext, text, 5)
            #var(6)
            os.system("cls")
            deathEnd()
    return enemyHp

def healthSystem():
    global elerhetoHealek
    healErtek = 20
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
    text = ["1000 pont - 1 életerő növelő"]
    curses.wrapper(centertext, text, 5)
    text = ["1000 pont - 1 életerő növelő", f"Pontjaid: {jatekos.Points}"]
    curses.wrapper(centertext, text, 5)
    #var(6)
    os.system("cls")
    commands = ["Vásárolsz életerő növelőt?", "Igen", "Nem"]
    choice = curses.wrapper(menu, commands)
    if choice == commands[1]:
        if jatekos.Points - 1000 < 0:
            text = ["Nincsen elegendő pontod."]
            curses.wrapper(centertext, text, 5)
            #var(6)
            os.system("cls")
            healthBuy()
        else:
            jatekos.Points -= 1000
            elerhetoHealek += 1
            text = [f"Életerő növelők száma eggyel megnövelve. Jelenlegi mennyiség: {elerhetoHealek}"]
            curses.wrapper(centertext, text, 5)
            #var(6)
            os.system("cls")
            if jatekos.Points > 1000:
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
        text = ["A város parkját kutatva egy táblára leszel figyelmes ami a városrész térképéta mutatja."]
        curses.wrapper(centertext, text)
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
            text = ["Hirtelen egy vörös macska fut végig az egyik erkélyen."]
            color = ["red"]
            curses.wrapper(centertext, text, 5, color)
            text= ["Hirtelen egy vörös macska fut végig az egyik erkélyen.", "Felettébb aranyos..."]#text = [f"{bcolors.FAIL}Feletébb aranyos...{bcolors.ENDC}"] ajsa nem tudsz magyarul
            szin = ["red"]
            curses.wrapper(centertext, text, 5, szin)
            os.system("cls")
            text = ["Egyszer csak leesik valami az erkélyről és nagy hanggal ér földet."]
            curses.wrapper(centertext, text, 5)
            os.system("cls")
            elerhetoFegyverek.append(fegyverek[2])
            text = [f"Gratulálok, ezennel feloldottad a következő fegyvert: {fegyverek[2].Nev} (Használhatóság: {fegyverek[2].Hasznalhato}, Sebzés: {fegyverek[2].Dmg})"]
            curses.wrapper(centertext, text, 5)
            os.system("cls")
        else:
            text = [f"Mivel nem találsz semmit visszatérsz a kapuhoz."]
            curses.wrapper(centertext, text, 5)
            # #var(5)
            os.system("cls")
    startRoom()

def room4():
    global szobaid
    szobaid = 4
    save()
    if roomFirst[szobaid] == True:
        roomFirst[szobaid] = False
        os.system("cls")
        text = ["A városka szűk utcáin barangolva már-mér elbóbiskolsz"]
        curses.wrapper(centertext, text, 5)
        # #var(6)
        text = ["Éppen visszafordulnál, mikor egy nyitott csatornafedél miatt a csatornába esel"]
        curses.wrapper(centertext, text, 5)
        # #var(76)
        text = ["Mire felelszmélsz már patkányok rohannak feléd."]
        curses.wrapper(centertext, text, 5)
        # #var(76)
        os.system("cls")
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
    jatekos.Hp -= 10
    text = [f"10 sebzést szenvedtél. Jelenlegi életerőd: {jatekos.Hp} HP"]
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
    text = ["ám a befelé vezető utat már egy eldőlt szekrény torlaszolja el."]
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
    if roomFirst[szobaid] == True:
        roomFirst[szobaid] = False
        text = ["Felérsz az emeletre. A szobában egy matracot találsz a földön, rajta egy kisfiúval."]
        curses.wrapper(centertext, text, 5)
        #var(75)
        text = ["Felérsz az emeletre. A szobában egy matracot találsz a földön, rajta egy kisfiúval.", "Mellette egy férfi térdel."]
        curses.wrapper(centertext, text, 5)
        #var(75)
        os.system("cls")
        text = [f"A fiam halálosan beteg. Gyógyszer kell neki, de én nem hagyhatom itt."]
        curses.wrapper(centertext, text, 5, ["cya"])
        #var(75)
        os.system("cls")
        commands = ["Hozol gyógyszert a kisfiúnak?", "Igen", "Nem"]
        choice = curses.wrapper(menu, commands)
        if choice == commands[1]:
            text = [f"Köszönöm...A neved?"]
            curses.wrapper(centertext, text, 5, ["cya"])
            #var(75)
            text = [f"Köszönöm...A neved?","Megmondod a neved."]
            #var(75)
            curses.wrapper(centertext, text, 5, ["cya", "cya"])
            text = [f"Köszönöm...A neved?","Megmondod a neved.",f"Köszönöm {jatekos.Nev}!"]
            curses.wrapper(centertext, text, 5, ["cya", "cya", ""])
            #var(75)
            text = [f"Köszönöm...A neved?","Megmondod a neved.",f"Köszönöm {jatekos.Nev}!","Elindulsz gyógyszert keresni."]
            curses.wrapper(centertext, text, 5, ["cya", "cya", "", ""])
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
            text = ["Nem tudsz semmi másra gondolni, csak hogy azt tetted amit muszáj volt."]
            curses.wrapper(centertext, text, 5)
            #var(75)
            text = ["Nem tudsz semmi másra gondolni, csak hogy azt tetted amit muszáj volt.","Sokkos állapotodban legjobbnak találod ha továbbhaladsz utadon,"]
            curses.wrapper(centertext, text, 5)
            #var(75)
            text = ["Nem tudsz semmi másra gondolni, csak hogy azt tetted amit muszáj volt.","Sokkos állapotodban legjobbnak találod ha továbbhaladsz utadon,","ezzel a kisfiút halálra ítélve."]
            #var(75)
            curses.wrapper(centertext, text, 5)
            os.system("cls")
    else:
        if quests["segitseg"] == True:
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
    if roomFirst[szobaid] == True:
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
        jatekos.Hp -= 15
        text = ["Éppen indulnál tovább, mikor egy zombihorda rohan feléd teljes sebességel.","Elkezdesz rohanni, de mielőtt a házhoz érnél elkapják a lábad.",f"15 sebzést szenvedtél. Jelenlegi életerőd: {jatekos.Hp} HP"]
        #var(75)
        curses.wrapper(centertext, text, 5)
        if jatekos.Hp <= 0:
            deathEnd()
        else:
            #var(75)
            text = ["Éppen indulnál tovább, mikor egy zombihorda rohan feléd teljes sebességel.","Elkezdesz rohanni, de mielőtt a házhoz érnél elkapják a lábad.",f"15 sebzést szenvedtél. Jelenlegi életerőd: {jatekos.Hp} HP","Szerencsére sikerül elérned az ajtóig, ám azt az annak rohanó zombik torlaszolják el,","ezzel eltorlaszolva a visszautat."]
            #var(75)
            curses.wrapper(centertext, text, 8)
            os.system("cls")
            room13()

def room13():
    global szobaid
    szobaid = 13
    save()
    if roomFirst[szobaid] == True:
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
        curses.wrapper(centertext, text, 5,["gre"])
        text = ["Mekkora szerencse, hogy pont megjelentél...",f"Lenne egy kérésem hozzád, bár nem éppen vagy abban a helyzetben, hogy visszautasítsd.","Hozd le nekem a két unokámat a 2. emeletről.",f'"Az emeleten van egy férfi, de valahogy úgyis megoldod..."',"Nincsen más lehetőséged, így elindulsz az épület folyosójára."]
        #var(75)
        curses.wrapper(centertext, text, 5,["gre"])
        os.system("cls")
    else:
        if quests["gyerekek"] == True:
            if quests["epuletKulcs"] == True:
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
                #var(75)
                quests["epuletKulcs"] = True
                text = ["Látom elhoztad nekem őket, köszönöm...",f'"Most vedd el ezt és tűnj el innen!"',"A kezedbe nyomott egy kulcsot..."]
                curses.wrapper(centertext, text, 5)
                #var(75)
                text = ["Látom elhoztad nekem őket, köszönöm...",f'"Most vedd el ezt és tűnj el innen!"',"A kezedbe nyomott egy kulcsot...",f'"Ezzel ki tudsz jutni..."']
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
        if roomFirst[szobaid] == True:
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
    save()
    if roomFirst[szobaid] == True:
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
        #var(75)
        text = ["Szörnyen érzed magad amiatt amit tettél, de tudod,"]
        #var(75)
        text = ["hogy az életed múlt rajta..."]
        #var(75)
        text = ["Kicsit megnyugszol, majd belépsz a lakásba, ahol a gyerekek vannak."]
        #var(75)
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
    #var(75)
    text = ["Egy 6 év körülinek tűnő kisfiú és a nővére áll veled szemben,"]
    #var(75)
    text = ["félelemmel a szemükben."]
    #var(75)
    text = ["Elmagyarázod nekik, hogy ki vagy és miért jöttél."]
    #var(75)
    text = ["A magyarázat hallatán közelebb lépnek hozzád."]
    #var(75)
    text = [f'{bcolors.WARNING}"Köszönjük szépen..."{bcolors.ENDC}']
    #var(75)
    text = ["Látszólag készen állnak követni téged."]
    #var(75)
    os.system("cls")
    room16()

def room18():
    global szobaid
    szobaid = 18
    save()
    if roomFirst[szobaid] == True:
        roomFirst[szobaid] = False
        text = ["Felérve a harmadik emeletre mozgásra leszel figyelmes..."]
        #var(75)
        text = ["Ekkor veszed észre a sarokban ülő, fertőzött (valamit mert még nem tudom mi legyen)."]
        #var(75)
        text = ["Amint észrevesz téged rádtámad."]
        #var(75)
        os.system("cls")
        fightSystem[opponents[2]]
        text = ["Szerencsére sikerült megölnöd..."]
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
                #var(75)
                os.system("cls")
                room18()
            else:
                text = ["Mindent megtaláltál már."]
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
                #var(75)
                os.system("cls")
                elerhetoFegyverek.append(fegyverek[6])
                text = [f"Gratulálok, ezennel feloldottad a következő fegyvert: {fegyverek[6].Nev} (Használhatóság: {fegyverek[6].Hasznalhato}, Sebzés: {fegyverek[6].Dmg})"]
                #var(75)
                os.system("cls")
                room18()
            else:
                text = ["Mindent megtaláltál már."]
                #var(75)
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
            text = ["A dobozok között nézelődve egyszercsak szuszogásra leszel figyelmes."]
            #var(75)
            text = ["Közelebb lépve egy juhászkutyát találsz összekuporodva az egyik dobozban."]
            #var(75)
            os.system("cls")
            elerhetoFegyverek.append(fegyverek[7])
            text = ["Gratulálok, ezzennel a kutya a társad."]
            #var(75)
            text = ["Harcokban tudod őt használni, melyekben fegyverként működik."]
            #var(75)
            text = [f"(Használhatóság: Végtelen, Sebzés: {fegyverek[7].Dmg})"]
            #var(75)
            os.system("cls")
            room19()
        else:
            text = ["A dobozok környékén már mindent fontosat megtaláltál."]
            #var(75)
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
            text = ["A padok között sétálva az egyiken észreveszel két elsősegély dobozt."]
            #var(75)
            text = ["Habár nyitva vannak, néhány kötszer még található bennük."]
            #var(75)
            os.system("cls")
            elerhetoHealek += 2
            text = [f"Gratulálok, találtál két életerő növelőt. Jelenlegi mennyiség: {elerhetoHealek} darab"]
            #var(75)
            os.system("cls")
        else:
            text = ["Már mindent megtaláltál."]
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
    #var(75)
    text = ["hogy amiért eddig harcoltál végre itt van előtted."]
    #var(75)
    text = ["Ez a kapu jelenti a kijutásodat."]
    #var(75)
    os.system("cls")
    text = ["A kapu előtt állsz, készen arra, hogy elhagyd ezt a helyet..."]
    #var(75)
    text = ["...ám ekkor érdekes hangot hallassz magad mögül."]
    #var(75)
    text = ["Hátrafordulva egy óriási mutáns zombit veszel észre."]
    #var(75)
    text = ["Mikor észrevesz ő is téged, teljes sebességel indul meg feléd."]
    #var(75)
    os.system("cls")
    fightSystem(opponents[6])
    text = ["Sikerült megölnöd a zombit, ám a végkimerülés szélén állsz."]
    #var(75)
    text = ["Ismét a kapu felé veszed az irányt."]
    #var(75)
    os.system("cls")
    if quests["varosKulcs"] == False:
        if quests["letra"] == True:
            text = ["Ott állva veszed észre, hogy a kapu zárva,"]
            #var(75)
            text = ["az idős férfitől kapott kulcs pedig nem nyitja..."]
            #var(75)
            text = ["Ekkor jut eszedbe a létra..."]
            #var(75)
            text = ["A sikátorban talált létrával sikerül átmásznod a kapun,"]
            #var(75)
            text = ["melynek a másik oldalán kimerülve érsz földet."]
            #var(75)
            os.system("cls")
            gameEnd()
        else:
            text = ["Ott állva jössz rá, hogy a kiút zárva,"]
            #var(75)
            text = ["neked pedig nincsen kulcsod."]
            #var(75)
            text = ["Megpróbálsz átmászni, de a kapu túl magas..."]
            #var(75)
            text = ["Kimerülten esel a földre..."]
            #var(75)
            text = [f"{bcolors.FAIL}Feladod...{bcolors.ENDC}"]
            #var(75)
            os.system("cls")
            deathEnd()
    else:
        text = ["Ott állva veszed észre, hogy a kapu zárva."]
        #var(75)
        text = ["Kipróbálod az idős férfitől kapott kulcsot ám az nem nyitja..."]
        #var(75)
        text = ["Ekkor jut eszedbe az apukától kapott kulcs."]
        #var(75)
        text = ["Belehelyezed a kulcslyukba és szerencsére kinyitja."]
        #var(75)
        text = ["Átlépsz a kapun és kimerülten esel a földre."]
        #var(75)
        os.system("cls")
        gameEnd()

def room22():
    global szobaid
    szobaid = 22
    commands = ["Ismét egy sikátorba lépsz.", "Körülnézek", "Visszamegyek"]
    choice = curses.wrapper(menu, commands)
    if choice == commands[1]:
        if quests["letra"] == False:
            quests["letra"] = True
            text = ["A sikátor falai közt barangolva egy létrára leszel figyelmes."]
            #var(75)
            text = ["Gondolván, hogy még jól jöhet, elhozod."]
            #var(75)
            os.system("cls")
        else:
            text = ["Már mindent megtaláltál."]
            #var(75)
            os.system("cls")
        room22()
    else:
        room20()

def gameEnd():
    text = ["Sikerült kijutnod a városból..."]
    #var(75)
    text = [f"{bcolors.FAIL}de vajon mi vár a város falain kívül?{bcolors.ENDC}"]
    #var(5)
    os.system("cls")
    text = [f"JÁTÉK VÉGE\n"]
    #var(2)
    text = [f"Elért pontszám: {jatekos.Points}"]
    #var(2)
    text = [f"Megszerzett fegyverek: {len(elerhetoFegyverek)}/{len(fegyverek)}"]
    #var(10)
    os.system("cls")
    endMenu()

def deathEnd():
    text = [f"{bcolors.FAIL}MEGHALTÁL{bcolors.ENDC}\n"]
    #var(2)
    text = [f"Elért pontszám: {jatekos.Points}"]
    #var(2)
    text = [f"Megszerzett fegyverek: {len(elerhetoFegyverek)}/{len(fegyverek)}"]
    #var(10)
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
