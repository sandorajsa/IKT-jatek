def startRoom():
    print("Úristen ijesztő.")
    options = ["Bal", "Jobb", "Előre"]
    userinput = ""
    while userinput not in options:
        userinput = input("Válassz egy útvonalat: ")
    if userinput == "Bal":
        room1()
    if userinput == "Jobb":
        room2()

def room1():
    print("1")
def room2():
    print("2")
def room3():
    print("3")