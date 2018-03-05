#!/usr/bin

import sys

import logging

from time import strptime

level = 20
module = []
module_exclude = []
num = 1024
min_time = 0
max_time = 1 << 63

log_file = 'log/logfile.txt'

colors = {
    logging.getLevelName('DEBUG'):    '\033[94m',
    logging.getLevelName('INFO'):     '\033[92m',
    logging.getLevelName('WARNING'):  '\033[93m',
    logging.getLevelName('ERROR'):    '\033[91m',
    logging.getLevelName('CRITICAL'): '\033[95m' + '\033[1m',
}
color_end = '\033[0m'

def parseLevel(l):
    try:
        ret = int(l)
        if ret >= 0:
            return ret
        else:
            raise Exception('invalid level name: ' + l)
    except:
        ret = logging.getLevelName(l)
        if type(ret) == int:
            if ret >= 0:
                return ret
            else:
                raise Exception('invalid level name: ' + l)
        else:
            raise Exception('invalid level name: ' + l)

dateformats = [
    '%y-%m-%d %H:%M:%S',
    '%Y-%m-%d %H:%M:%S',
    '%H:%M:%S',
    '%y-%m-%d',
    '%Y-%m-%d',
]

def parseDate(s):
    date = None
    for form in dateformats:
        try:
            date = strptime(s, form)
            break
        except:
            pass
    
    if date is None:
        raise Exception('invalid date format')
    else:
        res = date.tm_year  * 10000000000000
        res += date.tm_mon  * 100000000000
        res += date.tm_mday * 1000000000
        res += date.tm_hour * 10000000
        res += date.tm_min  * 100000
        res += date.tm_sec  * 1000
        return res

def extractNum(s):
    f = filter(str.isdigit, s)
    res = 0
    for i in f:
        res *= 10
        res += int(i)
    return res

#parsing stage

if len(sys.argv) > 1 and (sys.argv[1] == '-h' or sys.argv[1] == '--help'):
    print(
"""rlog -- Utility for reading the logs.

options:
\t-l - specify the lowest logging level to read (this level and higher), default is INFO.
\t-L - specifies the exact logging level to read.
\t-m - specifies a module logger to read.
\t-M - specifies a module logger to exclude.
\t-d - specifies the date of earlies messages to read.
\t-D - specifies the date of the last messages to read.
\t-n - specifies the maximum number of messages to read.

Message level can be DEBUG, INFO, WARNING, ERROR or CRITICAL, or numeric values (10 for DEBUG, 20 for INFO etc). Not case sensitive.

Dates are given in the format 'YYYY-MM-DD hh-mm-ss'. Year can be given as only two characters. Either YYYY-MM-DD or hh-mm-ss can be omitted.

Module is given in regular python syntax, example: '-m django.request' for messages emitted from djangos request module.

Example: 'rlog.py -L warning -m foo -M foo.tests -n 1000 -d 2017-01-01'
Reads 1000 messages of level WARNING since 1 jan 2017 from the log, from module foo excluding foo.tests
"""
    )
    exit()

try:
    i = 1
    
    while i < len(sys.argv):
      
        if sys.argv[i] == '-l':
            i += 1
            if i < len(sys.argv):
                level = parseLevel(sys.argv[i].upper())
        elif sys.argv[i] == '-L':
            i += 1
            if i < len(sys.argv):
                level = -parseLevel(sys.argv[i].upper())
        
        elif sys.argv[i] == '-m':
            i += 1
            if i < len(sys.argv):
                module.append(sys.argv[i])
        elif sys.argv[i] == '-M':
            i += 1
            if i < len(sys.argv):
                module_exclude.append(sys.argv[i])
        
        elif sys.argv[i] == '-n':
            i += 1
            if i < len(sys.argv):
                num = int(sys.argv[i])
        
        elif sys.argv[i] == '-d':
            i += 1
            if i < len(sys.argv):
                min_time = parseDate(sys.argv[i])
                assert min_time < max_time
        elif sys.argv[i] == '-D':
            i += 1
            if i < len(sys.argv):
                max_time = parseDate(sys.argv[i])
                assert min_time < max_time
        
        #else:
        #   raise Exception('invalid argument: ' + sys.argv[i])
        
        i += 1

except:
    print('invalid argument:', sys.argv[i])
    exit()

#file reading stage

filename = log_file

result = []

done = False

fileno = 0
filen = filename

while not done:
    try:
        lfile = open(filen, 'r')
    except:
        done = True
        break
    
    res = []
    for line in lfile:
        entry = line.split('\t')
        res.append(entry)
    
    tr = extractNum(res[0][0])
    if tr > max_time:
        res = []
    elif tr <= min_time:
        done = True
    
    if len(module) != 0:
        res = filter(lambda e: any(e[2].startswith(mod) for mod in module), res)
    if len(module_exclude) != 0:
        res = filter(lambda e: not any(e[2].startswith(mod) for mod in module_exclude), res)
    
    if level > 0:
        res = filter(lambda e: int(e[1]) >= level, res)
    elif level < 0:
        res = filter(lambda e: int(e[1]) == -level, res)
    
    if min_time > 0:
        res = filter(lambda e: extractNum(e[0]) > min_time, res)
    if max_time < 1 << 63:
        res = filter(lambda e: extractNum(e[0]) < max_time, res)
    
    res = [x for x in res]
    res.extend(result)
    result = res
    
    if len(result) >= num:
        result = result[-num:]
        done = True
    
    lfile.close()
    
    fileno += 1
    filen = filename + '.' + str(fileno)

#print query

for e in result:
    e[3] = e[3].replace('\\n', '\n').replace('\\t', '\t').replace('<%', '').replace('%>', '')
    sys.stdout.write('[ {0} ] '.format(e[0]))
    msg = ' | '.join(e[1:])
    if int(e[1]) in colors:
        msg = colors[int(e[1])] + msg + color_end
    sys.stdout.write(msg)

sys.stdout.flush()