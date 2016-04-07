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

def merge_training_set():
    cutoffLine('*')
    print 'Merge training set'
    start_time = time.time()

    positive_count = 0
    negative_count = 0
    total_count = 0

    total_file = file(PRE_DIR + '/' + 'train_set.csv', 'w')
    pos_file = file(PRE_DIR + '/' + 'positive_set.csv', 'w')
    neg_file = file(PRE_DIR + '/' + 'negative_set.csv', 'w')
    total_writer = csv.writer(total_file)
    pos_writer = csv.writer(pos_file)
    neg_writer = csv.writer(neg_file)

    for i in range(1, FILES-1):
        cutoffLine('-')
        print 'load train set %d' % i

        r_file  = file(PRE_DIR + '/' + 'set_%d.csv' % i)
        reader = csv.reader(r_file)
        for line in reader:
            doneCount(reader.line_num)
            line = map(int, line)
            if line[-1] == 1:
                positive_count += 1
                pos_writer.writerow(line)
            if line[-1] == 0:
                negative_count += 1
                neg_writer.writerow(line)
            total_count += 1
            total_writer.writerow(line)
        r_file.close()

    total_file.close()
    pos_file.close()
    neg_file.close()

    cutoffLine('-')
    # 44114
    print 'Positive Example: %d' % positive_count
    # 59373295
    print 'Negative Example: %d' % (total_count - positive_count)
    # 59417409
    print 'Total Example: %d' % total_count
    # 一致性判断
    print 'Is right? %s'%('Yes' if positive_count + negative_count == total_count else 'No')

    end_time = time.time()
    duration = timekeeper(start_time, end_time)
    cutoffLine('*')
    print 'It takes %s to merge training set and backup negative and positive set' % duration

if __name__ == '__main__':
    merge_training_set()
