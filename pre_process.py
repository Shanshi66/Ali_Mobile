# coding = utf-8
"""
    Transform date
    drop data of user who haven't buy anything
    @Author : Rosen
"""

import os
import csv
import time
from utility import cutoffLine, doneCount

def dataTransform():
    print 'start transform data...'
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
    print 'data transform finish!'

def transformDate(month,day):
    if month==11:return day-17
    else:return day+13

def drop_no_buy_user():
    cutoffLine('-')
    rfile = file('data/nuser.csv','r')
    reader = csv.reader(rfile)
    buyed_user = set()
    print 'user behavior stat'
    for line in reader:
        doneCount(reader.line_num)
        if int(line[2]) == 4: buyed_user.add(int(line[0]))
    rfile.close()
    print '\ndrop...'
    rfile = file('data/nuser.csv','r')
    wfile = file('data/nuser_cleaned','w')
    reader = csv.reader(rfile)
    writer = csv.writer(wfile)

    count = 0
    for line in reader:
        doneCount(reader.line_num)
        if int(line[0]) in buyed_user:
            writer.writerow(line)
            count += 1
    cutoffLine('-')
    print count
    rfile.close()
    wfile.close()

if __name__ == '__main__':
    #dataTransform()
    drop_no_buy_user()
