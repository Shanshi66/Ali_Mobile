import sys

def progressBar(done , total):
    cur_progress = float(done)/total*100
    if cur_progress == 100.0:
        sys.stdout.write("done!\n")
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
