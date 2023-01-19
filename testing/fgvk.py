import curses
import os
import time
import random
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
def gamestart():
    os.system("cls")
    commands = ["Üdvözlünk a 'lorem ipsum'","Új játék", "Folytatás"]
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
    gamertag = input("Elsőként add meg miként szólítsunk:\n")
    os.system("cls")
    commands = ["Válassz nehézségi fokozatot:","1", "2", "3"]
    jrng = 0
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
    startRoom()

def startRoom():
    commands = ["Megérkeztél a városba. Merre haladsz tovább?","Bal ", "Előre" , "Jobb", "Ki a városból"]
    userinput = curses.wrapper(menu, commands)
    if userinput == "Bal":
        room1()
    elif userinput == "Jobb":
        room2()
    elif userinput == "Előre":
        room3()
    else:
        return
def room1():
    print("1")
def room2():
    commands = ["Egy sikátorba érkeztél, fura hangokat hallasz", "Körbenézek", "Visszafutok"]
    choice = curses.wrapper(menu, commands)
    if choice == commands[1]:
        print(f"{bcolors.FAIL}Booo...{bcolors.ENDC}")
        print(f"Megijedsz és visszaszaladsz a városkapuhoz")
        commands = ["Merre haladsz tovább?","Bal ", "Előre", "Ki a városból"]
        userinput = curses.wrapper(menu, commands)
        if userinput == "Bal":
            room1()
        elif userinput == "Előre":
            room3()
        else:
            return
def room3():
    print("3")
def gameend():
    print("Game over")

