#coding: UTF-8

"""
    generate training set
    @Author : Rosen
"""

import csv
import os
import time
import random
from utility import progressBar, timekeeper, doneCount, cutoffLine
from utility import writeCSV, readCSV
from split import FILES

PRE_DIR = 'splited_data'
TOTAL = 59417409
POSITIVE = 44114
NEGATIVE = 59373295

def sampling():
    cutoffLine('*')
    print 'Sampling using EasyEnsemble method'
    start_time = time.time()

    TRAIN_SET = 'training_set'
    if not os.path.exists(TRAIN_SET): os.mkdir(TRAIN_SET)
    propotion = 10
    negative_size = POSITIVE * propotion
    r_file = file(PRE_DIR + '/negative_set.csv', 'r')
    reader = csv.reader(r_file)

    positive_set = readCSV(PRE_DIR + '/positive_set.csv', int)
    negative_set = []
    set_count = 0
    for line in reader:
        progressBar(reader.line_num, NEGATIVE)
        line = map(int, line)
        if line[-1] == 1: positive_set.append(line)
        if line[-1] == 0: negative_set.append(line)
        if len(negative_set) == negative_size or reader.line_num == NEGATIVE:
            set_count += 1
            training_set = positive_set + negative_set
            random.shuffle(training_set)
            file_name =  TRAIN_SET + '/' + '%d.csv'%set_count
            writeCSV(training_set, file_name)
            negative_set = []

    r_file.close()
    end_time = time.time()
    duration = timekeeper(start_time, end_time)
    cutoffLine('*')
    print 'It takes %s to sampling' % duration


if __name__ == '__main__':
    sampling()
