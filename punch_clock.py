'''
usage:
    clocking in: python punch_clock.py -i account1:account2
    clocking out: python punch_clock.py -o

usage: TODO
    run the script, automatically detects whether to clock in or out
    gives an option of categories to clock into based upon prvious values
    or specify a new one
'''

import sys
import datetime

# location of time card file
kJournal = "./sl_time.dat" 

# number of recent accounts to list as options
kAccountList = 5

# error message when you inevitably fail
kError = "How do people like you make it through the day? I mean honestly, this shouldn't be that hard and yet here we are. All you needed to do was enter a number within a range. Maybe you skipped the day in preschool when we went over numberlines. Regardless, I just wanted to let you know that you are a disappointment. Good day.\n"

def clockingOut(lines):
    tokens = lines[-1].split()
    return len(tokens) > 0 and tokens[0] == 'i'

def getPreviousAccounts(lines):
    # iterate backwards, getting 5 most recent accounts
    previous = []
    i = 1
    while len(previous) < kAccountList and i < len(lines):
        tokens = lines[-i].split()
        if len(tokens) > 0 and tokens[0] == 'i' and not tokens[-1] in previous:
            previous.append(tokens[-1])
        i += 1
    return previous  

def getAccount(lines):
    previous = getPreviousAccounts(lines)
    
    for i in range(len(previous)):
        print(f"enter ({i}) for {previous[i]}")
    print(f"enter {len(previous)} for custom")
    
    choice = int(input("choice:"))
    while (choice > len(previous) or choice < 0):
        print(kError)
        choice = int(input("I guess you can try again. Maybe be less of a disappointment this time? "))

    # enter custom account
    if choice == len(previous):
        return input("enter account:")

    # using a previously used account
    return previous[choice]

# Is this efficient? No
# Is this program performance critical? No
# Do I have other things that I need to do? Yes
def getLastAccount(lines):
    return getPreviousAccounts(lines)[0]

def debug():
    f = open(kJournal, 'r')
    lines = f.readlines()
    f.close()
    print(f"clockingOut call -> {clockingOut(lines)}")   
    print(f"getPreviousAccounts call -> {getPreviousAccounts(lines)}")  
    print(f"getLastAccount call -> {getLastAccount(lines)}") 

if __name__ == "__main__":
    debug()
    timestamp = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    f = open(kJournal, 'r')
    lines = f.readlines()
    f.close()

    f = open(kJournal, 'a')
    if clockingOut(lines):
        print("clocking out")
        f.write(f"o {timestamp}\n\n")
    elif len(sys.argv) == 2 and sys.argv[1] == '-n':
        print("clocking in with new account")
        f.write(f"i {timestamp} {getAccount(lines)}\n")
    else:
        print("clocking in to last account")
        f.write(f"i {timestamp} {getLastAccount(lines)}\n")
    f.close()