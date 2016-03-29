#coding: UTF-8

"""
    generate training set
    @Author : Rosen
"""

import csv
import os
import time
from utility import progressBar,timekeeper

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
        rfile.close()

    if result_set:
        for UI in UI_feature:
            if UI in result_set:
                writer.writerow(UI_feature[UI] + [1])
            else:
                writer.writerow(UI_feature[UI] + [0])
    else:
        for UI in UI_feature: writer.writerow(UI_feature)

    wfile.close()


if __name__ == '__main__':
    ## load the information of data set

    start_time = time.time()

    line_count = {}
    rfile = file(PRE_DIR + '/stat.csv','r')
    reader = csv.reader(rfile)
    for line in reader:
        line_count[line[0]] = int(line[1])
    rfile.close()

    for i in range(1,FILES + 1):
        if i == FILES:
            file_name = 'for_prediction.csv'
            extract_feature(file_name, line_count[file_name], i)
        else:
            file_name = '%d.csv' % i
            result_name = 'result_%d.csv' % i
            extract_feature(file_name, line_count[file_name], i, result_name)
    end_time = time.time()

    duration = timekeeper(start_time, end_time)
    print '-' * 50
    print 'It takes %s to generate training set' % duration
