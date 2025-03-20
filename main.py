import datetime
import os
#import time
#from time import strftime
#igotthis2
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
    "Hour 00-12":"I",
    "AM/PM":"p",
    "Minute 00-59":"M",
    "Second 00-59":"S",
    "Microsecond 000000-999999":"f",
    "UTC offset":"z",
    "Timezone":"Z",
    "Day number of year 001-366":"j",
    "Week number of year, Sunday as the first day of week, 00-53":"U",
    "Week number of year, Monday as the first day of week, 00-53":"W",
    "Line Break":"/",
    "Colon":":",
    "Comma":",",
    "Bar":"|",
    "Space":" ",
    "User Inputted String":"5"
}

mutable = {
    "Weekday":{"a","A","w"},
    "Month":{"b","B","m"},
    "Year":{"y","Y"},
    "Hour":{"I","H"},
    "Timezone":{"z","Z"},
    "Week # of year":{"U","W"}
}

default = "I:M:S p Z/A | d B Y/U | j"
clockSettings = "I:M:S p Z/A | d B Y/U | j"
preserveStrings = True
stringOrder = []

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
    prompt("Settings",["Edit Component","Advanced Settings","Reset Clock to Default", "Go Back"], [edit,advSettings,clockDefault,mainMenu])


def advSettings():
    prompt("Advanced Settings",
           ["Remove Component", "Add Component", "Clear Clock (For custom clocks)", "Get Clock Settings Code","Paste Clock Settings Code","Keep Default Strings", "Go Back"],
           [remove, add, clear, getClockStr,useClockStr, keepStr, settings])

def remove():
    global clockSettings
    clock()
    print("")

    componentList = []
    specialchars = "5/ :|,"
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

    pos = promptint(f"\nWhat component would you like to remove? (1-{len(clockSettings)})",[1, len(clockSettings)])
    clockSettings = clockSettings[:pos-1] + clockSettings[pos:]
    print("Successfuly removed component!")
    advSettings()

def add():
    global clockSettings
    global stringOrder
    specialchars = "5/ :|,"
    item = settingsPairs[prompt("What component would you like to add?",[x for x in settingsPairs.keys() if settingsPairs[x] in addable or settingsPairs[x] in specialchars],returns=True)]
    if item == "5":
        stringOrder.append(input("What would you like to include in this string? : "))
    clock()
    print("")

    componentList = []
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

    pos = promptint(f"Where would you would like to add this component before? (1-{len(clockSettings)})",[0, len(clockSettings)])
    if pos == 0:
        clockSettings = clockSettings + item
    else:
        clockSettings = clockSettings[:pos-1] + item + clockSettings[pos-1:]
    print("Successfuly added component!")
    advSettings()

def edit():
    global clockSettings
    possibleEdits = []
    for component in clockSettings:
        for key in mutable.keys():
            if component in mutable[key]:
                possibleEdits.append(key)

    chosen = prompt("What would you like to edit?\n(This will work poorly if there is more than one of the same type of setting in your clock)",possibleEdits,returns=True)
    usable = [x for x in mutable[chosen] if x not in clockSettings]
    usable = [[x for x in settingsPairs.keys() if i == settingsPairs[x]][0] for i in usable]

    try:
        x = usable[0]
    except IndexError:
        print("All versions of this setting are already in the clock")
        mainMenu()

    chosensquared = prompt(f"What would you like to change {chosen} to?",usable+["Go Back"],returns=True)
    replace = mutable[chosen] - {chosensquared}
    replace = [x for x in replace if x in clockSettings][0]

    if chosensquared == "Go Back":
        settings()

    elif chosensquared == "Hour 00-23":
        pos = clockSettings.find(replace)
        clockSettings = clockSettings[:pos] + settingsPairs[chosensquared] + clockSettings[pos + 1:]
        pos = clockSettings.find("p")
        clockSettings = clockSettings[:pos] + clockSettings[pos + 1:]

    elif chosensquared == "Hour 00-12":
        pos = clockSettings.find(replace)
        clockSettings = clockSettings[:pos] + settingsPairs[chosensquared] + clockSettings[pos + 1:]
        pos = clockSettings[pos:].find(" ") + pos
        print(pos)
        clockSettings = clockSettings[:pos+1] + "p" + clockSettings[pos+1:]

    else:
        pos = clockSettings.find(replace)
        clockSettings = clockSettings[:pos] + settingsPairs[chosensquared] + clockSettings[pos + 1:]

    print("Successfuly changed component!")
    settings()

def clear():
    global clockSettings
    clockSettings = ""
    print("Successfully cleared clock")
    settings()

def getClockStr():
    print(f"{clockSettings}#KeepDfStr:{preserveStrings}#{stringOrder}#")
    settings()

def useClockStr():
    global clockSettings
    global preserveStrings
    global stringOrder
    testSettings = input("Put code here: ")
    processedTestSettings = [testSettings[:testSettings.find("#")]]
    testSettings = testSettings[testSettings.find("#")+1:]

    while testSettings != "":
        processedTestSettings += [testSettings[:testSettings.find("#")]]
        testSettings = testSettings[testSettings.find("#") + 1:]

    try:
        clockSettings = processedTestSettings[0]
        if "True" in processedTestSettings[1]:
            preserveStrings = True
        elif "False" in processedTestSettings[1]:
            preserveStrings = False
        else:
            x = 1/0
        stringOrder = eval(processedTestSettings[2])
        print(stringOrder)
        clock()
        print("\nCode successfully applied!")
        settings()
    except (ValueError,IndexError,ZeroDivisionError):
        print("Code used contains illegal characters OR Is unable to be proccessed.")
        useClockStr()


def keepStr():
    global preserveStrings
    preserveStrings = not preserveStrings
    print("String preservation changed.")
    advSettings()


def clock():
    specialchars = "5/ :|,"
    x = 0
    for i in clockSettings:
        if i not in specialchars:
            if i not in "UWj":
                print(ctime.strftime(f"%{i}"), end = "")
            elif preserveStrings:
                if i == "U":
                    print("Week of the Year(Sun): " + ctime.strftime(f"%{i}"), end="")
                elif i == "W":
                    print("Week of the Year(Mon): " + ctime.strftime(f"%{i}"), end="")
                else:
                    print("Day of the Year: " + ctime.strftime(f"%{i}"), end="")
            else:
                print(ctime.strftime(f"%{i}"), end="")
        else:
            if i == "/":
                print("")
            if i == "5":
                print(stringOrder[x], end = "")
                x+=1
            if i in " :|,":
                print(i, end = "")

def clockDefault():
    global clockSettings
    clockSettings = default
    print("Succesfully reset clock settings!")
    settings()

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
