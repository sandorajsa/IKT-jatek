import curses
import os
def selectablemenu(stdscr,commands):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    selected_index = 0

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
            selected_index = max(selected_index - 1, 0)
        elif c == curses.KEY_DOWN:
            selected_index = min(selected_index + 1, len(commands) - 1)
        elif c == ord('\n'):
            return commands[selected_index]

def gamestart():
    os.system("cls")
    print("Üdvözlünk a játékban")
    gamertag = input("Elsőként add meg miként szólítsunk:\n\t")
    os.system("cls")
    
    commands = ["1", "2", "3"]
    szam = curses.wrapper(selectablemenu, commands)
    if szam == "1":
        jhp = 100
        jdmg = 15
    elif szam == "2":
        jhp = 75
        jdmg = 10
    elif szam == "3":
        jhp = 50
        jdmg = 5
    startRoom()

def startRoom():
    print("Úristen ijesztő.")
    options = ["Bal", "Jobb", "Előre"]
    userinput = ""
    while userinput not in options:
        userinput = input("Válassz egy útvonalat: ")
    if userinput == "Bal":
        room1()
    elif userinput == "Jobb":
        room2()
    elif userinput == "Előre":
        room3()

def room1():
    print("1")
def room2():
    print("2")
def room3():
    print("3")

gamestart()
