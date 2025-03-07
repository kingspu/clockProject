import datetime
import os
import time
from time import strftime

clockSettings = "I:M:S p Z/A | d B Y/5U | 5j"
stringOrder = ["Week of the Year: ","Day of the Year: "]
def prompt(demand: str, choices: list[str], funcs = None, returns = False, fLtr = False):
    print(demand)
    if fLtr == False:
        for i in range(len(choices)):
            print(f"[{i+1}] : {choices[i]}")
        choice = input("What would you like to do? : ")
        if choice.isdigit():
            if int(choice) in range(1,len(choices)+1):
                if returns == False:
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

        fLtrList = [x[0].upper() for x in choices]
        if "Exit" in choices:
            fLtrList.insert(fLtrList.index("E"),"X")
            fLtrList.remove("E")
        if "Display Current Time" in choices:
            fLtrList.insert(fLtrList.index("D"),"T")
            fLtrList.remove("D")

        if choice[0].upper() in fLtrList:
            if returns == False:
                funcs[fLtrList.index(choice[0].upper())]()
            else:
                return choices[fLtrList.index(choice[0].upper())]
        else:
            print("Please enter an accepted value.")
            return prompt(demand, choices, funcs, returns, fLtr)



def settings():
    print("This is currently not implemented")
    time.sleep(1)
    mainMenu()
    prompt("Settings",[],[])


def clock():
    stringNum = 0
    print("Welcome to Daniel's Clock Program!")
    specialchars = "/5 :|,"
    for i in clockSettings:
        if i not in specialchars:
            print(ctime.strftime(f"%{i}"), end = "")
        else:
            if i == "/":
                print("")
            if i == "5":
                print(stringOrder[stringNum],end = "")
                stringNum += 1
            if i in " :|,":
                print(i, end = "")






def exit():
    print("You have successfuly exited the program")
    quit(0)


def mainMenu():
    os.system("cls")
    global ctime
    ctime = datetime.datetime.now()
    clock()
    prompt("",["Display Current Time","Settings","Exit"],[mainMenu,settings,exit], fLtr = True)
mainMenu()
