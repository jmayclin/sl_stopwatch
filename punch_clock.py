'''
punch_clock.py
james mayclin
    run the script, automatically detects whether to clock in or out
    gives an option of categories to clock into based upon prvious values
    or specify a new one
'''

import sys
import datetime

# location of time card file
kTimeCard = "./timecard.dat" 

# number of recent accounts to list as options
kAccountList = 5

# error message when you inevitably fail

# a text wrapping library woul make this much nicer
# but I also don't care to deal with that right now
# nor, I suspect, will anyone want to in the future
kError = ("\n" +
    "How do people like you make it through the day? I mean\n" +
    "honestly, this shouldn't be that hard and yet here we\n" +
    "are. All you needed to do was enter a number within a\n" +
    "range. Maybe you skipped the day in preschool when we\n" +
    "went over numberlines. Regardless, I just wanted to let\n" +
    "you know that you are a disappointment. Good day.\n"
)

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
        choice = int(input("I guess you can try again.\nMaybe be less of a disappointment this time? "))

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
    f = open(kTimeCard, 'r')
    lines = f.readlines()
    f.close()
    print(f"clockingOut call -> {clockingOut(lines)}")   
    print(f"getPreviousAccounts call -> {getPreviousAccounts(lines)}")  
    print(f"getLastAccount call -> {getLastAccount(lines)}") 

if __name__ == "__main__":
    debug()
    timestamp = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    f = open(kTimeCard, 'r')
    lines = f.readlines()
    f.close()

    f = open(kTimeCard, 'a')
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