import datetime
import collections

kJournal = "timecard.dat"
kTimecard_Url = "https://axess.sahr.stanford.edu/group/guest/employee-center"

# col vals are 1, 2, 3, 4
# 1 and 3 are clock in time
# 2 and 4 are clock out time
# row values correspond to dates
# row value 0 is first day of time period
kInputID = "PUNCH_TIME_{col}${row}"
kInputForm = "document.getElementById(\"{id}\").value = \"{time}\""

def parse_time(line):
    tokens = line.split()
    date = datetime.datetime.strptime(tokens[1], "%Y/%m/%d").date()
    time = datetime.datetime.strptime(tokens[2], "%H:%M:%S").time()
    return date, time    

def count_hours():
    lines = []
    with open(kJournal, 'r') as f:
        lines = f.readlines()
    lines = [line for line in lines if not line.isspace() and len(line) > 0]
    hours = collections.defaultdict(datetime.timedelta)
    for i in range(len(lines)):
        if lines[i][0] == 'i':
            print("found clock in")
            date_in, time_in = parse_time(lines[i])
            date_out, time_out = parse_time(lines[i + 1])
            if date_in != date_out:
                raise ValueError('There are two days here. I don\'t feel like dealing with this')
            hours[date_in] += datetime.datetime.combine(datetime.date.today(), time_out) - datetime.datetime.combine(datetime.date.today(), time_in)
    return hours

# I won't ever be using this script in January, so if this issue bothers you fix it yourself.
def get_time_period(hours):
    last = max(hours.keys())
    choices = {}
    if last.day >= 16:
        choices[0] = datetime.date(year = last.year, month = last.month, day = 16)
        choices[1] = datetime.date(year = last.year, month = last.month, day = 1)
    else:
        choices[0] = datetime.date(year = last.year, month = last.month,     day = 1)
        choices[1] = datetime.date(year = last.year, month = last.month - 1, day = 16)
    print("Choose pay period starting:")
    for key in choices:
        print(f"({key}) - {choices[key]}")

    return choices[int(input("I didn't bother with error checking so you only get one shot at this:"))]

def make_cursed(index, timestamp, clocking_in):
    column = 1
    if not clocking_in:
        column = 2
    inputID = kInputID.format(row = index, col = column)
    value_line = kInputForm.format(id = inputID, time = timestamp)
    print(value_line)

def output_cursed_language(hours, time_period):
    start = time_period
    end = None
    if start.day == 16:
        end = datetime.date(year = start.year, month = start.month + 1, day = 1) - datetime.timedelta(days = 1)
    else:
        end = datetime.date(year = start.year, month = start.month, day = 15) - datetime.timedelta(days = 1)
    index = 0
    increment = datetime.timedelta(days = 1)
    current = start
    while(current <= end):
        if not current in hours:
            current += increment
            index += 1
            continue
        diff = hours[current]
        hour = diff.seconds // 3600
        minute = (diff.seconds // 60) % 60
        second = diff.seconds - hour * 3600 - minute * 60
        make_cursed(index, "00:00:00", True)
        make_cursed(index, f"{hour}:{minute}:{second}", False)

        current += increment
        index += 1
    

if __name__ == "__main__":
    hours = count_hours()
    print(hours)
    time_period = get_time_period(hours)
    output_cursed_language(hours, time_period)
