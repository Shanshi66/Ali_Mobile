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


class ItemBasedCF:
    def __init__(self,trainData,items,itemClassified_category,itemClassified_geohash):
        self.trainData = trainData
        self.items = items
        self.itemClassified_category=itemClassified_category
        self.itemClassified_geohash=itemClassified_geohash

    def ItemSimilarity(self):
        C = dict()  #物品-物品的共现矩阵
        N = dict()  #物品被多少个不同用户购买
        for user,items in self.trainData.items():
            for i in items.keys():
                N.setdefault(i,0)
                N[i] += 1
                C.setdefault(i,{})
                for j in items.keys():
                    if i == j : continue
                    C[i].setdefault(j,0)
                    C[i][j] += 1
        #计算相似度矩阵
        self.W = dict()
        for i,related_items in C.items():
            self.W.setdefault(i,{})
            for j,cij in related_items.items():
                self.W[i][j] = cij / (math.sqrt(N[i] * N[j]))
        return self.W

    #给用户user推荐，前K个相关用户
    def Recommend(self,user,K=3,N=10):
        rank = dict()
        action_item = self.train[user]     #用户user产生过行为的item和评分
        for item,score in action_item.items():
            for j,wj in sorted(self.W[item].items(),key=lambda x:x[1],reverse=True)[0:K]:
                if j in action_item.keys():
                    continue
                rank.setdefault(j,0)
                rank[j] += score * wj
        return dict(sorted(rank.items(),key=lambda x:x[1],reverse=True)[0:N])

if __name__== "__main__":
    items,itemClassified_category,itemClassified_geohash = processItemData('train_item.csv')
    trainData = processUserData('train_user.csv',items)
    print len(trainData)
