import csv

def parseEntry(entry):
    priorityValues = ['High', 'Medium', 'Low', 'Debug']
    if entry[1] == "match":
        s = raw_input("Input for string '%s': " % entry[2])
        if entry[2] in s:
            try:
                p = int(entry[0])
            except (ValueError, IndexError):
                return 'Invalid priority # for database entry: ' + str(entry)
            else:
                return '{} level threat found (using blacklist method {})'.format(priorityValues[p-1], entry[1])
    return False

with open('spamtrap.csv', 'rb') as csvfile:
    spamdb = csv.reader(csvfile, delimiter=',')
    for entry in spamdb:
        print parseEntry(entry)