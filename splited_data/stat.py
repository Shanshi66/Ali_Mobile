"""
    @function : get useful information of the datasets
    @Author : Rosen
"""

import csv
import os
import sys
import time

PRE_DIR = os.path.dirname(__file__)
FILES = 22

sys.path.append(PRE_DIR + '/..')
from utility import doneCount,timekeeper

def lineCount():
    stat_file = file(PRE_DIR + '/stat.csv','w')
    writer = csv.writer(stat_file)
    for i in range(1,FILES+1):
        print '\n' + '-'*50

        if i == FILES: file_name = 'for_prediction.csv'
        else: file_name = '%d.csv' % i

        file_path = PRE_DIR + '/' + file_name

        print 'processing %s' % file_name

        rfile = file(file_path,'r')
        reader = csv.reader(rfile)
        count = 1
        for line in reader:
            doneCount(reader.line_num)
            count += 1
        writer.writerow([file_name, count])
        rfile.close()
    stat_file.close()

if __name__ == '__main__':
    start_time = time.time()
    lineCount()
    end_time = time.time()
    duration = timekeeper(start_time, end_time)
    print '-' * 50
    print 'It takes %s '% duration
