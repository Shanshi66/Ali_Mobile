#coding: UTF-8

"""
    generate training set
    @Author : Rosen
"""

import csv
import os
import time
from utility import progressBar, timekeeper, doneCount, cutoffLine

FILES = 22
PRE_DIR = 'splited_data'

def extract_feature(fileName, line_count, start_date, result_name = ''):
    r_name = PRE_DIR + '/' + file_name
    w_name = PRE_DIR + '/set_' + file_name
    r_file = file(r_name, 'r')
    w_file = file(w_name, 'w')
    reader = csv.reader(r_file)
    writer = csv.writer(w_file)

    UI_feature = {}
    for line in reader:
        progressBar(reader.line_num, line_count)
        UI = (int(line[0]),int(line[1]))
        if UI not in UI_feature: UI_feature[UI] = [0]*40
        ##  0 ～  9 前十天浏览量统计
        ## 10 ～ 19 前十天收藏量统计
        ## 20 ～ 29 前十天加入购物车统计
        ## 30 ～ 39 前十天购买量统计

        index = int(line[5]) - start_date
        if int(line[2]) == 1 : UI_feature[UI][index] += 1
        if int(line[2]) == 2 : UI_feature[UI][10+index] += 1
        if int(line[2]) == 3 : UI_feature[UI][20+index] += 1
        if int(line[2]) == 4 : UI_feature[UI][30+index] += 1

    r_file.close()

    ## 打标签
    result_set = set()
    if result_name:
        r_name = PRE_DIR + '/' + result_name
        r_file = file(r_name, 'r')
        reader = csv.reader(r_file)
        for line in reader: result_set.add((int(line[0]), int(line[1])))
        r_file.close()

    if result_set:
        for UI in UI_feature:
            if UI in result_set:
                writer.writerow(UI_feature[UI] + [1])
            else:
                writer.writerow(UI_feature[UI] + [0])
    else:
        for UI in UI_feature: writer.writerow(UI_feature[UI])

    w_file.close()



def generate_training_set():
    ## load the information of data set
    start_time = time.time()

    line_count = {}
    rfile = file(PRE_DIR + '/stat.csv','r')
    reader = csv.reader(rfile)
    for line in reader:
        line_count[line[0]] = int(line[1])
    rfile.close()

    cutoffLine('*')
    print 'Generate training set'

    for i in range(FILES,FILES + 1):
        cutoffLine('-')
        if i == FILES:
            file_name = 'for_prediction.csv'
            print 'Extract feature from %s'%file_name
            extract_feature(file_name, line_count[file_name], i)
        else:
            file_name = '%d.csv' % i
            print 'Extract feature from %s and tag it'%file_name
            result_name = 'result_%d.csv' % i
            extract_feature(file_name, line_count[file_name], i, result_name)
    end_time = time.time()

    duration = timekeeper(start_time, end_time)
    cutoffLine('*')
    print 'It takes %s to generate training set' % duration

def merge_training_set():
    cutoffLine('*')
    print 'Merge training set'

    start_time = time.time()

    positive_count = 0
    total_count = 0
    w_file = file(PRE_DIR + '/' + 'train_set.csv', 'w')
    writer = csv.writer(w_file)

    for i in range(1, FILES):
        cutoffLine('-')
        print 'load train set %d' % i

        r_file  = file(PRE_DIR + '/' + 'set_%d.csv' % i)
        reader = csv.reader(r_file)
        for line in reader:
            doneCount(reader.line_num)
            line = map(int, line)
            if line[-1] == 1: positive_count += 1
            total_count += 1
            writer.writerow(line)
        r_file.close()

    w_file.close()

    cutoffLine('-')
    print 'Total Example: %d' % total_count
    print 'Positive Example: %d' % positive_count
    print 'Negative Example: %d' % (total_count - positive_count)

    end_time = time.time()
    duration = timekeeper(start_time, end_time)
    cutoffLine('*')
    print 'It takes %s to merge training set' % duration

if __name__ == '__main__':
    # generate_training_set()
    merge_training_set()
