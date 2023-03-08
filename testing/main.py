import curses
import time
import keyboard
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
def var(ido):
    startido = time.time()
    elteltido = 0
    while elteltido < int(ido):
        elteltido = time.time() - startido
        if keyboard.is_pressed('space'):
            time.sleep(0.5)
            return True
    return True
def fileolvas():
    f = open(f"1.txt", "r", encoding="UTF-8")
    for sor in f: 
        asd = sor.strip().split(';') 
        strtext = asd[0]
        text = strtext.strip().split('+')
        strszin = asd[1]
        szin = strszin.strip().split('+')
        varido = asd[2]
        curses.wrapper(centertext,text,varido, szin)
fileolvas()