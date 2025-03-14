import datetime
import os
#import time
#from time import strftime

settingsPairs = {
    "Weekday, short version":"a",
    "Weekday, full version":"A",
    "Weekday as a number 0-6, 0 is Sunday":"w",
    "Day of month 01-31":"d",
    "Month name, short version":"b",
    "Month name, full version":"B",
    "Month as a number 01-12":"m",
    "Year, short version, without century":"y",
    "Year, full version":"Y",
    "Hour 00-23":"H",
    "Hour 00-12	":"I",
    "AM/PM":"p",
    "Minute 00-59":"M",
    "Second 00-59":"S",
    "Microsecond 000000-999999":"f",
    "UTC offset":"z",
    "Timezone":"Z",
    "Day number of year 001-366":"j",
    "Week number of year, Sunday as the first day of week, 00-53":"U",
    "Week number of year, Monday as the first day of week, 00-53":"W"
}


clockSettings = "I:M:S p Z/A | d B Y/U | j"
#stringOrder = ["Week of the Year: ","Day of the Year: "]

def prompt(demand: str, choices: list[str], funcs = None, returns = False, fltr = False):
    print(demand)
    if not fltr:
        for i in range(len(choices)):
            print(f"[{i+1}] : {choices[i]}")
        choice = input("What would you like to do? : ")
        if choice.isdigit():
            if int(choice) in range(1,len(choices)+1):
                if not returns:
                    funcs[int(choice) - 1]()
                else:
                    return choices[int(choice)-1]
            else:
                print("Please enter an accepted value.")
                return prompt(demand, choices, funcs, returns)
        else:
            print("Please enter an accepted value.")
            return prompt(demand,choices,funcs,returns)
    else:
        for i in range(len(choices)):
            if choices[i] not in ["Exit","Display Current Time"]:
                print(f"[{choices[i][0]}] : {choices[i]} | " , end = "")
            elif choices[i] == "Exit":
                print(f"[X] : {choices[i]}")
            elif choices[i] == "Display Current Time":
                print(f"[T] : {choices[i]} | ", end = "")

        choice = input("What would you like to do? : ")

        fltrlist = [x[0].upper() for x in choices]
        if "Exit" in choices:
            fltrlist.insert(fltrlist.index("E"),"X")
            fltrlist.remove("E")
        if "Display Current Time" in choices:
            fltrlist.insert(fltrlist.index("D"),"T")
            fltrlist.remove("D")

        if choice[0].upper() in fltrlist:
            if not returns:
                funcs[fltrlist.index(choice[0].upper())]()
            else:
                return choices[fltrlist.index(choice[0].upper())]
        else:
            print("Please enter an accepted value.")
            return prompt(demand, choices, funcs, returns, fltr)

def promptint(demand: str, range : list[int]):
    chosenint = input(f"{demand} : ")
    if chosenint.isdigit() and int(chosenint) >= range[0] and int(chosenint) <= range[1]:
        return int(chosenint)
    else:
        print("Please choose and accepted value.")
        return promptint(demand,range)


def settings():
    global changedPos
    global clockSettings
    global settingNames
    global settingVals
    global removable
    global addable
    settingNames = list(settingsPairs.keys())
    settingVals = "".join(list(settingsPairs.values()))
    removable = [x for x in list(settingsPairs.values()) if x in clockSettings]
    addable = [x for x in list(settingsPairs.values()) if x not in clockSettings]
    prompt("Settings",["Edit Component","Advanced Settings", "Go Back"], [edit,advSettings,mainMenu])


def advSettings():
    prompt("Advanced Settings",
           ["Remove Component", "Add Component", "Clear Clock (For custom clocks)", "Get Clock Settings Code","Paste Clock Settings Code", "Go Back"],
           [remove, add, clear, getClockStr,useClockStr, settings])


def remove():
    global clockSettings
    removableStrings = [x for x in settingsPairs.keys() if settingsPairs[x] in removable]
    item = settingsPairs[prompt("Removable Items:",removableStrings, returns=True)]
    clockSettings = clockSettings[:clockSettings.find(item)] + clockSettings[clockSettings.find(item)+1:]
    print("Successfuly removed component!")
    settings()


def add():
    global clockSettings
    item = settingsPairs[prompt("What component would you like to add?",[x for x in settingsPairs.keys() if settingsPairs[x] in addable],returns=True)]
    clock()
    print("")

    componentList = []
    specialchars = "/ :|,"
    for i in clockSettings:
        if i not in specialchars:
            componentList.append(ctime.strftime(f"%{i}"))
        else:
            componentList.append(i)

    i = 0
    for x in componentList:
        i += 1
        if i%4 != 0:
            print(f" ({x}@{i}) #",end ="")
        else:
            print(f" ({x}@{i})")
    else:
        print(" (0 for The End)")
    pos = promptint(f"Where would you would like to add this component? (1-{len(clockSettings)})",[0, len(clockSettings)])
    if pos == 0:
        clockSettings = clockSettings + item
    else:
        clockSettings = clockSettings[:pos-1] + item + clockSettings[pos-1:]
    print("Successfuly added component!")
    settings()

def edit():
    pass
    print("Successfuly changed component!")
    settings()

def clear():
    global clockSettings
    clockSettings = ""
    print("Successfully cleared clock")
    settings()

def getClockStr():
    print(clockSettings)
    settings()

def useClockStr():
    global clockSettings
    testSettings = input("Put code here: ")
    try:
        clockSettings = testSettings
        clock()
        print("\nCode successfully applied!")
        settings()
    except ValueError:
        print("Code used contains illegal characters.")
        useClockStr()



def clock():
    specialchars = "/ :|,"
    for i in clockSettings:
        if i not in specialchars:
            print(ctime.strftime(f"%{i}"), end = "")
        else:
            if i == "/":
                print("")
            if i in " :|,":
                print(i, end = "")

def exit():
    print("You have successfuly exited the program")
    quit(0)


def mainMenu():
    os.system("cls")
    global ctime
    ctime = datetime.datetime.now()
    print("Welcome to Daniel's Clock Program!")
    clock()
    prompt("", ["Display Current Time","Settings","Exit"], [mainMenu,settings,exit], fltr= True)
mainMenu()
