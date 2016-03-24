#coding=utf-8
"""
	Author : Rosen
	Date : 2016.03.24
"""

import csv
import os
import math

user_file = 'data/user.csv'
item_file = 'data/item.csv'
nuser_file = 'data/nuser.csv'

def dataTransform():
	user_file = file('data/user.csv','r')
	new_user_file = file('data/nuser.csv','w')
	reader = csv.reader(user_file)
	writer = csv.writer(new_user_file)

	data_set = []
	for line in reader:
		if reader.line_num == 1: continue
		if reader.line_num%10000 == 0: print reader.line_num
		date , hour = line[5].split(' ')
		year , month ,day = date.split('-')
		line[5] = transformDate(int(month),int(day))
		line.append(hour)
		data_set.append(line)

	data_set.sort(dateCmp)

	for line in data_set:
		writer.writerow(line)

	user_file.close()
	new_user_file.close()

def transformDate(month,day):
	if month==11:return day-17
	else:return day+13

def dateCmp(x,y):
	if int(x[5])<int(y[5]):return -1
	elif int(x[5])>int(y[5]):return 1
	else:
		if x[6]<y[6]:return -1
		elif x[6]==y[6]:return 0
		else: return 1
