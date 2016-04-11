"""
Author : Rosen
Date : 2016.03.24
"""

import csv
from utility import cutoffLine, doneCount

def stat():
    cutoffLine('-')
    print 'stat some information...'
    user_file = file('data/nuser.csv','r')
    item_file = file('data/item.csv','r')
    stat_file = open('data/stat.txt','w')


    row_count = 0
    user_set = set()
    sub_item_set = set()
    all_item_set = set()
    category_set = set()
    user_geo_count = 0
    item_geo_count = 0

    reader = csv.reader(item_file)
    for line in reader:
        doneCount(reader.line_num)
        if reader.line_num == 1: continue
        if line[1]: item_geo_count += 1
        category_set.add(line[2])
        sub_item_set.add(line[0])

    reader = csv.reader(user_file)
    for line in reader:
        doneCount(reader.line_num)
        row_count += 1
        user_set.add(line[0])
        all_item_set.add(line[1])
        if line[3]: user_geo_count += 1

    interact_item_set = all_item_set & sub_item_set

    stat_file.write('%s : %s\n'%(u'Total Count',row_count))
    stat_file.write('%s : %s\n'%(u'User Count',len(user_set)))
    stat_file.write('%s : %s\n'%(u'All Item Count',len(all_item_set)))
    stat_file.write('%s : %s\n'%(u'Sub Item Count',len(sub_item_set)))
    stat_file.write('%s : %s %f\n'%(u'Interact Item Count',
                                    len(interact_item_set),
                                    float(len(interact_item_set))/len(sub_item_set)))
    stat_file.write('%s : %s\n'%(u'Category Count',len(category_set)))
    stat_file.write('%s : %s\n'%(u'User Geo Count',user_geo_count))
    stat_file.write('%s : %s\n'%(u'Item Geo Count',item_geo_count))

    stat_file.close()
    user_file.close()
    item_file.close()

if __name__ == '__main__':
    stat()
