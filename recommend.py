from math import sqrt

def processItemData(fileName):
    inputData=open(fileName)
    itemAmount=0
    itemClassified_category={}
    itemClassified_geohash={}
    items={}
    for line in inputData:
        #if itemAmount == 10000:break
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
        #if itemAmount==10000:break
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
    def __init__(self,trainData):
        self.trainData=trainData
    def sim_item(self,t1,t2):
        si = {}
        for user in self.trainData[t1]:
            if user in self.trainData[t2]:si[user]=1
        n = len(si)
        print "share user:%d"%n
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

    def sim_distance(self,t1,t2):
        si={}
        for user in self.trainData[t1]:
            if user in self.trainData[t2]:si[user]=1
        print "share user:%d"%len(si)
        if len(si)==0:return 0
        sum_of_squares=sum([pow(self.trainData[t1][u]-self.trainData[t2][u],2)
                            for u in self.trainData[t1] if u in self.trainData[t2]])

        return 1/(1+sqrt(sum_of_squares))

    def topK(self,item,k=10,similarity=sim_item):
        scores=[(similarity(item,other),other) for other in self.trainData if other!=item]
        scores.sort()
        scores.reverse()
        return scores[0:k]

    def calculateSimilarItems(self,n=10):
        result={}
        c=0
        for item in self.trainData:
            c+=1
            if c%100==0:print "%d / %d"%(c,len(trainData))
            scores=self.topK(item,k=n,similarity=self.sim_distance)
            result[item]=scores
        return result

    def transform(self,data):
        userItemData={}
        for item,userlist in data.items():
            for user,rating in userlist.items():
                userItemData.setdefault(user,{})
                userItemData[user][item]=rating
        return userItemData

    def getRecommendedItems(self,items,user):
        userItemData=self.transform(self.trainData)
        userRatings=userItemData[user]
        scores={}
        totalSim={}
        for (item,rating) in userRatings.items():
            for (similarity,item2) in items[item]:
                print similarity
                print item2
                if item2 in userRatings:continue

                scores.setdefault(item2,0)
                scores[item2]+=similarity*rating

                totalSim.setdefault(item2,0)
                totalSim[item2]+=similarity
        rankings=[(score/totalSim[item],item) for item,score in scores.items()]
        rankings.sort()
        ranking.reverse()
        return rankings

if __name__== "__main__":
    items,itemClassified_category,itemClassified_geohash = processItemData('train_item.csv')
    userData,trainData = processUserData('train_user.csv',items)
    itembase=itemBaseCF(trainData)
    itemsMatch=itembase.calculateSimilarItems(n=10)
    for user in userData:
        print len(itembase.getRecommendedItems(itemsMatch,user))
