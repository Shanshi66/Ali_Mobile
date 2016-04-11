#coding=utf-8
import csv
import os
import time
import random
from utility import progressBar, timekeeper, doneCount, cutoffLine
from utility import writeCSV, readCSV
from split import FILES
import sys

PRE_DIR = 'splited_data'
TOTAL_10 = 56992193
POSITIVE_10 = 44114
NEGATIVE_10 = 56948079

TOTAL_7 = 46748293
POSITIVE_7 = 46802
NEGATIVE_7 = 46701491

def sampling(window, proportion):
    cutoffLine('*')
    start_time = time.time()
    print 'sampling with propotion %d...' % proportion
    exec('negative_needed = POSITIVE_%d * propotion' % window)
    sample_times = 20
    exec('mod = NEGATIVE_%d / sample_times' % window)
    exec('negative_eachtime = negative_needed / sample_times')
    training_set = readCSV(PRE_DIR + '/positive_set.csv', int)

    ## sampling negative example
    rfile = file(PRE_DIR + '/' + 'negative_set.csv', 'r')
    reader = csv.reader(rfile)
    negative_tmp = []
    for line in reader:
        exec('progressBar(reader.line_num, NEGATIVE_%d)' % window)
        negative_tmp.append(map(int, line))
        if reader.line_num % mod == 0:
            random.shuffle(negative_tmp)
            training_set.extend(negative_tmp[0:negative_eachtime])
            negative_tmp = []
    rfile.close()

    wfile = file('data/training_set_%d_%d.csv' % (window, propotion), 'w')
    writer = csv.writer(wfile)
    random.shuffle(training_set)
    writer.writerows(training_set)
    wfile.close()

    cutoffLine('-')
    exec('real_proportion = (len(training_set)- POSITIVE_%d) / float(POSITIVE_%d)'%(window, window))
    print "Real proportion: %f" % real_proportion
    cutoffLine('*')
    end_time = time.time()
    duration = timekeeper(start_time, end_time)
    print 'It takes %s to sampling with proportion %d'%(duration, proportion)

if __name__ == '__main__':
    if len(sys.argv) < 3: print 'Need sample window and propotion'
    else:
        window = int(sys.argv[1])
        propotion = int(sys.argv[2])
        print 'Window %d dataset' % window
        global PRE_DIR
        PRE_DIR = 'splited_data_%d' % window
        sampling(window, propotion)
