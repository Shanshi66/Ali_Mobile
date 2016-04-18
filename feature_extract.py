#coding=UTF-8
import csv
import os
import time
import sys
import random
import pickle
from utility import progressBar, timekeeper, doneCount, cutoffLine
from utility import writeCSV, readCSV
from split import FILES, TOTAL_DAY

PRE_DIR = 'splited_data'
ci_sale = {}

def extract_feature(window, actday, file_name, line_count, start_date, result_name = ''):
    r_name = PRE_DIR + '/' + file_name
    w_name = PRE_DIR + '/set_' + file_name
    r_file = file(r_name, 'r')
    w_file = file(w_name, 'w')
    reader = csv.reader(r_file)
    writer = csv.writer(w_file)

    ## 统计同类商品排名，为了避免使用未来信息
    ci_rank = {}
    for c in ci_sale:
        ## 统计(actday-window)之前商品销量
        ci_rank[c] = {}
        for item in ci_sale[c]:
            ci_rank[c][item] = sum(ci_sale[c][item][0:actday-window])
        ## 销量排名；销量好的排名在后，方便处理没有销量的商品(设为0)
        rank_list = sorted(ci_rank[c].iteritems(), key = lambda x: x[1])
        for index, item in enumerate(rank_list):
            item = list(item)
            item[1] = index + 1
            rank_list[index] = item
        ci_rank[c] = dict(rank_list)

    UI_feature = {}
    for line in reader:
        progressBar(reader.line_num, line_count)
        UI = (int(line[0]),int(line[1]),int(line[4]))
        if UI not in UI_feature: UI_feature[UI] = [0]*(window*4)
        ## 4种行为统计
        index = int(line[5]) - start_date
        if int(line[2]) == 1 : UI_feature[UI][index] += 1
        if int(line[2]) == 2 : UI_feature[UI][window+index] += 1
        if int(line[2]) == 3 : UI_feature[UI][2*window+index] += 1
        if int(line[2]) == 4 : UI_feature[UI][3*window+index] += 1

    r_file.close()

    ## 商品同类排名
    for UI in UI_feature:
        if ci_rank[UI[2]].has_key(UI[1]): UI_feature[UI].append(ci_rank[UI[2]][UI[1]])
        else: UI_feature[UI].append(0)

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
            if (UI[0],UI[1]) in result_set:
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
            extract_feature(window, i+window, file_name, line_count[file_name], i)
        elif i == FILES - 1:
            file_name = 'test.csv'
            print 'Extract feature from %s'%file_name
            result_name = 'result_%s'%file_name
            extract_feature(window, i+window, file_name, line_count[file_name], i, result_name)
        else:
            file_name = '%d.csv' % i
            print 'Extract feature from %s and tag it'%file_name
            result_name = 'result_%d.csv' % i
            extract_feature(window, i+window, file_name, line_count[file_name], i, result_name)
    end_time = time.time()

    duration = timekeeper(start_time, end_time)
    cutoffLine('*')
    print 'It takes %s to generate training set' % duration

def global_feature():
    cutoffLine('-')
    print 'Generate global feature'
    # 统计每种商品每天销量，为统计每种商品在同类商品种排名服务， 为了避免使用未来信息
    global ci_sale
    if os.path.exists('data/ci_sale.pkl'):
        ci_sale_file = open('data/ci_sale.pkl', 'rb')
        ci_sale = pickle.load(ci_sale_file)
        # for c in ci_rank: print ci_rank[c]
        ci_sale_file.close()
    else:
        u_file = file('data/nuser.csv', 'r')
        u_reader = csv.reader(u_file)
        ci_sale = {}
        for line in u_reader:
            doneCount(u_reader.line_num)
            item = int(line[1])
            behavior = int(line[2])
            category = int(line[4])
            date = int(line[5])
            if not ci_sale.has_key(category): ci_sale[category] = {}
            if behavior == 4:
                if not ci_sale[category].has_key(item): ci_sale[category][item] = [0]*(TOTAL_DAY+1)
                ci_sale[category][item][date] += 1

        ci_sale_file = open('data/ci_sale.pkl', 'wb')
        pickle.dump(ci_sale, ci_sale_file)
        ci_sale_file.close()
        u_file.close()


if __name__ == '__main__':
    if len(sys.argv) < 2: print 'Need window size'
    else:
        window = int(sys.argv[1])
        global_feature()
        generate_training_set(window)
