import sys
import csv

def progressBar(done , total):
    cur_progress = float(done)/total*100
    if cur_progress == 100.0:
        sys.stdout.write("\ndone!")
    else:
        sys.stdout.write('\r'+'%6.2f'%cur_progress + r'%')
    sys.stdout.flush()

def doneCount(done):
    sys.stdout.write('\r'+'%6d'%done)
    sys.stdout.flush()

def cutoffLine(line_type):
    if line_type == '*': print '\n' + '*' * 50
    if line_type == '-': print '\n' + '-' * 50

def timekeeper(start_time,end_time):
    duration = end_time - start_time
    if duration > 3600:
        duration = float(duration)/3600
        unit = 'h'
    elif duration > 60:
        duration = float(duration)/60
        unit = 'm'
    else:
        unit = 's'
    return '%.2f%s' % (duration, unit)

def writeCSV(items, file_name):
    w_file = file(file_name, 'w')
    writer = csv.writer(w_file)
    for item in items: writer.writerow(item)
    w_file.close()

def readCSV(file_name,fun):
    r_file = file(file_name, 'r')
    reader = csv.reader(r_file)
    result = []
    for line in reader:
        result.append(map(fun, line))
    r_file.close()
    return result

def loadItemSubset():
    cutoffLine('-')
    print 'load item subset'
    rfile = file('data/item.csv','r')
    reader = csv.reader(rfile)
    item_set = set()
    for line in reader:
        doneCount(reader.line_num)
        if reader.line_num == 1: continue
        item_set.add(int(line[0]))
    return item_set

def dropItemsNotInSet(result, subset):
    result_after = set()
    for item in result:
        if item[1] in subset: result_after.add(item)
    return result_after
