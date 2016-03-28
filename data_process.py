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


def dateCmp(x,y):
    if int(x[5])<int(y[5]):return -1
    elif int(x[5])>int(y[5]):return 1
    else:
        if x[6]<y[6]:return -1
        elif x[6]==y[6]:return 0
        else: return 1
