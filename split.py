"""
    split data set
    @Author : Rosen
"""

import csv
from utility import progressBar,timekeeper,cutoffLine
import time

PERIOD = 11
TOTAL_DAY = 31
FILES = TOTAL_DAY - PERIOD + 2
#DATASET_SIZE = 23291027
DATASET_SIZE = 22427352
PRE_DIR = 'splited_data'
DATA_SET = 'data/nuser_cleaned.csv'

def splitData():
    stat_file = file('splited_data/stat.csv','w')
    stat_writer = csv.writer(stat_file)
    for i in range(1,FILES+1):
        cutoffLine('-')
        print 'Split dataset %d: ' % i
        rfile = file(DATA_SET,'r')
        reader = csv.reader(rfile)
        j = i + 10
        if j != TOTAL_DAY + 1:
            if j == TOTAL_DAY:
                train_file_name = 'test.csv'
                result_file_name = 'result_test.csv'
            else:
                train_file_name = '%d.csv'%i
                result_file_name = '%s_%d.csv'%('result',i)
            train_file = file(PRE_DIR + '/' + train_file_name,'w')
            result_file = file(PRE_DIR + '/' + result_file_name,'w')
            train_writer = csv.writer(train_file)
            result_writer = csv.writer(result_file)
            train_count = 0
            result_count = 0
            for line in reader:
                progressBar(reader.line_num, DATASET_SIZE)
                if int(line[5]) >= i and int(line[5]) < j:
                    train_writer.writerow(line)
                    train_count += 1
                if int(line[5]) == j and int(line[2]) == 4:
                    result_writer.writerow([line[0],line[1]])
                    result_count += 1
            stat_writer.writerow([train_file_name, train_count])
            stat_writer.writerow([result_file_name, result_count])
            train_file.close()
            result_file.close()
        else:
            forpredict_file_name = 'for_prediction.csv'
            train_file = file(PRE_DIR + '/' + forpredict_file_name,'w')
            train_writer = csv.writer(train_file)
            train_count = 0
            for line in reader:
                progressBar(reader.line_num,DATASET_SIZE)
                if int(line[5]) >= i and int(line[5]) < j:
                    train_writer.writerow(line)
                    train_count += 1
            stat_writer.writerow([forpredict_file_name, train_count])
            train_file.close()
        rfile.close()

if __name__ == '__main__':
    print 'Start split data'
    cutoffLine('*')
    start_time = time.time()
    splitData()
    end_time = time.time()
    duration = timekeeper(start_time,end_time)
    cutoffLine('*')
    print 'It takes ' + duration + ' to split dataset.'
