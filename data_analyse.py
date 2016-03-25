"""
Author : Rosen
Date : 2016.03.24
"""

import csv

def stat():
    user_file = file('data/user.csv','r')
    item_file = file('data/item.csv','r')
    stat_file = open('data/stat.txt','w')
    reader = csv.reader(user_file)

    row_count = 0
    user_set = set()
    item_set = set()
    category_set = set()
    user_geo_count = 0
    item_geo_count = 0

    for line in reader:
        if reader.line_num == 1 : continue
        if reader.line_num%10000 == 0:print reader.line_num
        row_count += 1
        user_set.add(line[0])
        item_set.add(line[1])
        if line[3]: user_geo_count += 1

    reader = csv.reader(item_file)
    for line in reader:
        if reader.line_num == 1: continue
        if reader.line_num%10000 == 0:print reader.line_num
        if line[1]: item_geo_count += 1
        category_set.add(line[2])
        item_set.add(line[0])

    stat_file.write('%s : %s\n'%(u'Total Count',row_count))
    stat_file.write('%s : %s\n'%(u'User Count',len(user_set)))
    stat_file.write('%s : %s\n'%(u'Item Count',len(item_set)))
    stat_file.write('%s : %s\n'%(u'Category Count',len(category_set)))
    stat_file.write('%s : %s\n'%(u'User Geo Count',user_geo_count))
    stat_file.write('%s : %s\n'%(u'Item Geo Count',item_geo_count))

    stat_file.close()
    user_file.close()
    item_file.close()

if __name__ == '__main__':
    print '-----------------------------------'
    print 'stat some information...'
    stat()
