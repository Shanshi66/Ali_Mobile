def processItemData(fileName):
    inputData=open(fileName)
    itemAmount=0
    itemClassified_category={}
    itemClassified_geohash={}
    items={}
    for line in inputData:
        if itemAmount == 0:
            itemAmount=itemAmount+1
            continue
        item,item_geohash,item_category = line.strip().split(',')
        items[item]=(item_geohash,item_category)
        itemClassified_category.setdefault(item_category,[])
        itemClassified_category[item_category].append(item)
        if item_geohash:
            itemClassified_geohash.setdefault(item_geohash,[])
            itemClassified_geohash[item_geohash].append(item)
        itemAmount=itemAmount+1
    inputData.close()
    return items,itemClassified_category,itemClassified_geohash

def processUserData(fileName,items):
    inputData=open(fileName)
    trainData={}
    itemAmount=0
    for line in inputData:
        if itemAmount == 0:
            itemAmount=itemAmount+1
            continue
        user,item,score,user_geohash,item_category,time =line.strip().split(',')
        trainData.setdefault(user,{})
        if items.has_key(item):
            item_geohash=items[item][0]
        else:
            item_geohash=''
            trainData[user][(item,item_geohash)]=(score,time,user_geohash)
        itemAmount=itemAmount+1
        print itemAmount
    inputData.close()
    return trainData


if __name__== "__main__":
    items,itemClassified_category,itemClassified_geohash = processItemData('train_item.csv')
    trainData = processUserData('train_user.csv',items)
    print len(trainData)
