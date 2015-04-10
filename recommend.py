from math import sqrt

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
    userData={}
    trainData={}
    itemAmount=0
    for line in inputData:
        if itemAmount == 0:
            itemAmount=itemAmount+1
            continue
        user,item,score,user_geohash,item_category,time =line.strip().split(',')
        userData.setdefault(user,{})
        trainData.setdefault(item,{})
        trainData[item][user]=int(score)
        if items.has_key(item):
            item_geohash=items[item][0]
        else:
            item_geohash=''
            userData[user][(item,item_geohash)]=(int(score),time,user_geohash)
        itemAmount=itemAmount+1
        print itemAmount
    inputData.close()
    return userData,trainData

class itemBaseCF:
    def __init__(trainData):
        self.trainData=trainData
    def sim_item(t1,t2):
        si = {}
        for user in self.trainData[t1]:
            if user in self.trainData[t2]:si[user]=1
        n = len(si)
        if n==0:return 0;
        sum1=sum([self.trainData[t1][u] for u in si])
        sum2=sum([self.trainData[t2][u] for u in si])

        sum1Sq=sum([pow(self.trainData[t1][u],2) for it in si])
        sum2Sq=sum([pow(self.trainData[t2][u],2) for it in si])

        pSum =sum([self.trainData[t1][u]*self.trainData[t2][u] for u in si])

        num=pSum-(sum1*sum2/n)
        den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
        if den==0:return 0

        r=num/den
        return r

    def sim_distance(t1,t2):
        si={}
        for user in self.trainData[t1]:
            if user in self.trainData[t2]:si[user]=1

        if len(si)==0:return 0
        sum_of_squares=sum([pow(self.trainData[t1][u]-self.trainData[t2][u],2)
                            for u in self.trainData[t1] if u in self.trainData[t2]])

        return 1/(1+sqrt(sum_of_squares))

    def topK(item,k=10,similarity=sim_item):
        scores=[(similarity(item,other),other) for other in self.trainData if other!=item]
        scores.sort()
        scores.reverse()
        return scores[0:k]

    def calculateSimilarItems(n=10):
        result={}
        c=0
        for item in self.trainData:
            c+=1
            if c%100==0:print "%d / %d"%(c,len(trainData))
            scores=topK(item,k=n,similarity=sim_item)
            result[item]=scores
        return result

if __name__== "__main__":
    items,itemClassified_category,itemClassified_geohash = processItemData('train_item.csv')
    userData,trainData = processUserData('train_user.csv',items)
