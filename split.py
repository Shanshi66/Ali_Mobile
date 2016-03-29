"""
    split data set
    @Author : Rosen
"""

import csv
from utility import progressBar,timekeeper
import time

PERIOD = 11
FILES = 31 - PERIOD + 2
DATASET_SIZE = 23291027

DATA_SET = 'data/nuser.csv'

def splitData():
    for i in range(1,FILES+1):
        print '-'*50
        print 'Split dataset 1 %d: ' % i
        rfile = file(DATA_SET,'r')
        reader = csv.reader(rfile)
        j = i + 10
        if j != 32:
            train_file = file('splited_data/%d.csv'%i,'w')
            result_file = file('splited_data/%s_%d.csv'%('result',i),'w')
            train_writer = csv.writer(train_file)
            result_writer = csv.writer(result_file)
            for line in reader:
                progressBar(reader.line_ num,DATASET_SIZE)
                if int(line[5]) >= i and int(line[5]) < j: train_writer.writerow(line)
                if int(line[5]) == j and int(line[2]) == 4: result_writer.writerow([line[0],line[1]])
            train_file.close()
            result_file.close()
        else:
            train_file = file('splited_data/for_prediction.csv','w')
            train_writer = csv.writer(train_file)
            for line in reader:
                progressBar(reader.line_num,DATASET_SIZE)
                if int(line[5]) >= i and int(line[5]) < j: train_writer.writerow(line)
            train_file.close()
        rfile.close()

if __name__ == '__main__':
    start_time = time.time()
    splitData()
    end_time = time.time()
    duration = timekeeper(start_time,end_time)
    print '='*50
    print 'It takes ' + duration + ' to split dataset.'
