# coding = utf-8
"""
    Transform date
    drop data of user who haven't buy anything
    @Author : Rosen
"""

import os
import csv
import time

def dataTransform():
    minday = 50
    maxday = -1

    user_file = file('data/user.csv','r')
    new_user_file = file('data/nuser.csv','w')
    reader = csv.reader(user_file)
    writer = csv.writer(new_user_file)

    for line in reader:
        if reader.line_num == 1:continue
        if reader.line_num%10000 == 0: print reader.line_num
        date , hour = line[5].split(' ')
        year , month ,day = date.split('-')
        line[5] = transformDate(int(month),int(day))
        if line[5] < minday : minday = line[5]
        if line[5] > maxday : maxday = line[5]
        line.append(hour)
        writer.writerow(line)

    user_file.close()
    new_user_file.close()

    print minday,maxday

def transformDate(month,day):
    if month==11:return day-17
    else:return day+13

if __name__ == '__main__':
    print '------------------------------'
    print 'start transform data...'
    t0 = time.time()
    dataTransform()
    t1 = time.time()
    print 'data transform finish!'
    print 'I take %f s'%(t1-t0)
