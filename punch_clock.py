'''
usage:
    clocking in: python punch_clock.py -i account1:account2
    clocking out: python punch_clock.py -o
'''

import sys
import datetime

kJournal = "./sl_time.dat"

if __name__ == "__main__":
    flag = ""
    account = ""
    if len(sys.argv) == 3 and sys.argv[1] == "-i":
        flag = "i"
        account = sys.argv[2]
    elif len(sys.argv) == 2 and sys.argv[1] == "-o":
        flag = "o"
        account = ""
    else:
        raise NameError("invalid arguments")

    current = datetime.datetime.now()
    timestamp = current.strftime("%Y/%m/%d %H:%M:%S")
    with open(kJournal, 'a') as f:
        f.write(f"{flag} {timestamp} {account}\n")

    print(f"wrote \"{flag} {timestamp} {account}\" to {kJournal}")
    
