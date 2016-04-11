#coding=UTF-8
import csv
import os
import time
import sys
import random
from utility import progressBar, timekeeper, doneCount, cutoffLine
from utility import writeCSV, readCSV
from split import FILES, TOTAL_DAY

PRE_DIR = 'splited_data'

def extract_feature(window, file_name, line_count, start_date, result_name = ''):
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
        if UI not in UI_feature: UI_feature[UI] = [0]*(window*4)
        ##  4种行为统计
        index = int(line[5]) - start_date
        if int(line[2]) == 1 : UI_feature[UI][index] += 1
        if int(line[2]) == 2 : UI_feature[UI][window+index] += 1
        if int(line[2]) == 3 : UI_feature[UI][2*window+index] += 1
        if int(line[2]) == 4 : UI_feature[UI][3*window+index] += 1

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
                writer.writerow(list(UI) + UI_feature[UI] + [1])
            else:
                writer.writerow(list(UI) + UI_feature[UI] + [0])
    else:
        for UI in UI_feature: writer.writerow(list(UI) + UI_feature[UI])

    w_file.close()

def generate_training_set(window):
    start_time = time.time()
    global PRE_DIR, FILES
    PRE_DIR = 'splited_data_%d'%window
    FILES = TOTAL_DAY - window +1

    ## load the information of data set
    line_count = {}
    rfile = file(PRE_DIR + '/stat.csv','r')
    reader = csv.reader(rfile)
    for line in reader:
        line_count[line[0]] = int(line[1])
    rfile.close()

    cutoffLine('*')
    print 'Generate training set with window %d'%window

    for i in range(1,FILES + 1):
        cutoffLine('-')
        if i == FILES:
            file_name = 'for_prediction.csv'
            print 'Extract feature from %s'%file_name
            extract_feature(window, file_name, line_count[file_name], i)
        elif i == FILES - 1:
            file_name = 'test.csv'
            print 'Extract feature from %s'%file_name
            result_name = 'result_%s'%file_name
            extract_feature(window, file_name, line_count[file_name], i, result_name)
        else:
            file_name = '%d.csv' % i
            print 'Extract feature from %s and tag it'%file_name
            result_name = 'result_%d.csv' % i
            extract_feature(window, file_name, line_count[file_name], i, result_name)
    end_time = time.time()

    duration = timekeeper(start_time, end_time)
    cutoffLine('*')
    print 'It takes %s to generate training set' % duration

def global_feature():
    u_file = file('data/nuser.csv', 'r')

    ci_rank = {}

    for line in u_file:
        item = int(line[1])
        behavior = int(line[2])
        if behavior == 4:
            if ci_rank.has_key(item):
                ci_rank[]

    u_file.close()

if __name__ == '__main__':
    if len(sys.argv) < 2: print 'Need window size'
    else:
        window = int(sys.argv[1])
        global_feature()
        generate_training_set(window)
