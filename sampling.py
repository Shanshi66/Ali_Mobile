#coding=utf-8
import csv
import os
import time
import random
from utility import progressBar, timekeeper, doneCount, cutoffLine
from utility import writeCSV, readCSV
from split import FILES

PRE_DIR = 'splited_data'
TOTAL = 56992193
POSITIVE = 44114
NEGATIVE = 56948079

def sampling(proportion):
    cutoffLine('*')
    start_time = time.time()
    print 'sampling with propotion %d...'%proportion
    negative_needed = POSITIVE * proportion
    sample_times = 10
    mod = NEGATIVE / sample_times
    negative_eachtime = negative_needed / sample_times

    training_set = readCSV(PRE_DIR + '/positive_set.csv', int)

    ## sampling negative example
    rfile = file(PRE_DIR + '/' + 'negative_set.csv', 'r')
    reader = csv.reader(rfile)
    negative_tmp = []
    for line in reader:
        progressBar(reader.line_num, NEGATIVE)
        negative_tmp.append(map(int, line))
        if reader.line_num % mod == 0:
            random.shuffle(negative_tmp)
            training_set = training_set + negative_tmp[0:negative_eachtime]
            negative_tmp = []
    rfile.close()

    wfile = file('data/training_set_%d.csv'%proportion, 'w')
    writer = csv.writer(wfile)
    random.shuffle(training_set)
    writer.writerows(training_set)
    wfile.close()

    cutoffLine('-')
    print "Real proportion: %f" %((len(training_set)-POSITIVE) / float(POSITIVE))
    cutoffLine('*')
    end_time = time.time()
    duration = timekeeper(start_time, end_time)
    print 'It takes %s to sampling with proportion %d'%(duration, proportion)

if __name__ == '__main__':
    sampling(10)
