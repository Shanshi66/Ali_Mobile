import csv
import DataProcess
import random
import os
import numpy as np
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import train_test_split
from sklearn import preprocessing


subfile = "dutir_tianchi_recom_predict_luosen.csv"
tdata = "data_transformed.csv"

def loadPosibility():
	rfile = file("userBuyPosibility.csv","r")
	reader = csv.reader(rfile)
	posibility={}
	for line in reader:
		posibility[line[0]]=float(line[1])
	rfile.close()
	return posibility

def cartBuy(month,day,hour,percent,p):
	posibility = loadPosibility();
	data_file = file("%s_%s_%s_%s.csv"%(month,day,hour,percent),"r")
	result_file = file("cartBuy_%s%s%s.csv"%(month,day,hour),"w")
	submit_file = file(subfile,"w")

	reader = csv.reader(data_file)
	writer = csv.writer(result_file)
	swriter = csv.writer(submit_file)

	cart_set=set()
	buy_set=set()
	for user_id,item_id,behavior_type,item_category,date,h in reader:
		if behavior_type=="3":cart_set.add((user_id,item_id))
		if behavior_type=="4":buy_set.add((user_id,item_id))

	writer.writerow(["userid","itemid"])
	swriter.writerow(["userid","itemid"])

	i=0
	for c in cart_set:
		if c in buy_set:continue
		if posibility.has_key(c[0]) and posibility[c[0]] < p:continue
		writer.writerow(c)
		swriter.writerow(c)
		i+=1
	print i

	data_file.close()
	result_file.close()
	submit_file.close()


def userBuyPosibility():
	rfile = file("data34.csv","r")
	wfile = file("userBuyPosibility.csv","w")

	reader = csv.reader(rfile)
	writer = csv.writer(wfile)

	posibility={}
	cart_set = {}
	buy_set ={}
	data_set=[]

	data_size = len(data_set)
	for line in reader:
		index=int(line[4])
		if index > data_size:
			data_set.append([])
			data_size=len(data_set)
		data_set[index-1].append(tuple(line))

	for i in range(data_size):
		if i>0:
			for d in data_set[i]:
				if d[2]=="4":
					if buy_set.has_key(d[0]):buy_set[d[0]].append(d[1])
					else:buy_set[d[0]]=[d[1]]
			for u in buy_set:
				if not u in cart_set: continue
				count=0
				for item in buy_set[u]:
					if item in cart_set[u]:count=count+1
				p = float(count)/len(cart_set[u])
				if posibility.has_key(u):posibility[u].append(p)
				else:posibility[u]=[p]
			buy_set={}
		cart_set={}
		for d in data_set[i]:
			if d[2]=="3":
				if cart_set.has_key(d[0]):cart_set[d[0]].append(d[1])
				else:cart_set[d[0]]=[d[1]]

	for u in posibility:
		posibility[u]=sum(posibility[u])/len(posibility[u])

	for u in posibility:
		writer.writerow([u,posibility[u]])

	rfile.close()
	wfile.close()



def cartBuy2(month,day,hour,step,proportion):
    itemHot = DataProcess.loadfile("item_stat.csv")
    newDate = DataProcess.transformDate(month,day)

    itemHotDic={}
    for item in itemHot:
    	item[1]=int(item[1])
    	itemHotDic[item[0]]=item[1]

    itemHot.sort(lambda x,y:cmp(y[1],x[1]))
    
    #rfile=open("cleaned_data.csv","r")

    rfile = "data_after_%s_%s.csv"%(month,day-step+2)
    if not os.path.exists(rfile):
    	print rfile+" not exists"
    	return
    rfile=open("data_after_%s_%s.csv"%(month,day-step+2),"r")
    wfile=open("answer.csv","w")
    
    reader = csv.reader(rfile)
    writer = csv.writer(wfile)
    #[user_id,item_id,behavior_type,user_geohash,item_category,newDate,int(hour)
    
    cart_set=set()
    buy_set=set()
    
    ans_set={}
    ui_scan_stat={}

    for user,item,behavior,geo,cate,date,h in reader:
        date = int(date)
        h = int(h)
        behavior=int(behavior)
        if date >= newDate:
        	if not ui_scan_stat.has_key((user,item)):ui_scan_stat[(user,item)]=[0]*step
        	if behavior==1:ui_scan_stat[(user,item)][date+step-32]+=1
        	if behavior==4:ui_scan_stat[(user,item)][-1]=1
        if (date==newDate and h>hour) or (date>newDate):
            if behavior==3:cart_set.add((user,item))
            if behavior==4:buy_set.add((user,item))

    wp = {}
    for item in ui_scan_stat:
    	if ui_scan_stat[item][-1]==1:continue
    	wp[item]=ui_scan_stat[item][-3:-1]
    
    writer.writerow(["userid","itemid"])
    
    for item in cart_set:
        if item in buy_set:continue
        if not ans_set.has_key(item[0]):ans_set[item[0]]=[]
        # if wp.has_key(item):
        # 	ans_set[item[0]].append((item[1],wp[item][-1]))
        # else:
        # 	ans_set[item[0]].append((item[1],0))
        ans_set[item[0]].append((item[1],itemHotDic[item[1]]))

    for user in ans_set:
    	ans_set[user].sort(i_scan_cmp)
    	slen = int(len(ans_set[user])*0.9)
    	for i,item in enumerate(ans_set[user]):
    		if len(ans_set[user])<50:
    			writer.writerow([user,item[0]])
    			continue
    		if i<slen:
    			writer.writerow([user,item[0]])


    #logRes = LR("sample_data_%s_%s.csv"%(step,proportion))

    # count=0
    # for ui in wp:
    # 	if logRes.predict([wp[ui]])==1:
    # 		count+=1
    # 		writer.writerow(ui)
    # print count

    # for user in ans_set:
    # 	for item in ans_set[user]:
    # 		if wp.has_key((user,item)):
    # 			if logRes.predict([wp[(user,item)]])==1:
    # 				writer.writerow([user,item])
    # 		else:
    # 			writer.writerow([user,item])

    #stat = [len(ans_set[it]) for it in ans_set]
    #stat.sort()
    #for it in stat:print it
    

    
    rfile.close()
    wfile.close()

def i_scan_cmp(x,y):
	if x[1]<y[1]:return 1
	elif x[1]>y[1]:return -1
	else: return 0

def formTrainSet(step=7):
	wfile = file("train_data_%s.csv"%step,"w")
	writer = csv.writer(wfile)

	stat_set={}
	if os.path.exists("trainSet_temp.csv"):
		print "trainSet_temp.csv exists"
		rfile = file("trainSet_temp.csv","r")
		reader = csv.reader(rfile)
		for user,item,date,b1,b2,b3,b4 in reader:
			stat_set[(user,item,date)]=[int(b1),int(b2),int(b3),int(b4)]
		rfile.close()
	else:
		rfile = file("cleaned_data.csv","r")
		wfile = file("trainSet_temp.csv","w")
		reader = csv.reader(rfile)
		writer = csv.writer(wfile)

		for user,item,behavior,geo,cate,date,h in reader:
			if reader.line_num%10000==0:print reader.line_num
			if not stat_set.has_key((user,item,date)):stat_set[(user,item,date)]=[0,0,0,0]
			behavior = int(behavior)
			if behavior==1:stat_set[(user,item,date)][0]+=1
			if behavior==2:stat_set[(user,item,date)][1]=1
			if behavior==3:stat_set[(user,item,date)][2]=1
			if behavior==4:stat_set[(user,item,date)][3]=1

		for it in stat_set:
			writer.writerow([it[0],it[1],it[2],stat_set[it][0],stat_set[it][1],stat_set[it][2],stat_set[it][3]])

		rfile.close()
		wfile.close()

	stat_set = sorted(stat_set.iteritems(),key = lambda it:it[0][2])
	print len(stat_set)

	print stat_set[0]

	train_set = [[]]*(30/step)
	temp_set={}
	b=0
	for i,user_item_date in enumerate(stat_set):
		if i%10000==0:print i
		user =user_item_date[0][0]
		item =user_item_date[0][1]
		date =int(user_item_date[0][2])

		if (date/step)>len(train_set)-1:
			print date
			break
		index = date/step
		if index > b:
			for it in temp_set:
				if temp_set[it][-1]==1:continue
				train_set[b].append(temp_set[it][:-1])
			temp_set={}
			b=index
		if not temp_set.has_key((user,item)):temp_set[(user,item)]=[0]*(step+2)
		day = date%step
		if day > 0:
			temp_set[(user,item)][day-1]=user_item_date[1][0]
			if user_item_date[1][3]==1:temp_set[(user,item)][step+1]=1
		if day==0:
			temp_set[(user,item)][step-1]=user_item_date[1][0]
			if user_item_date[1][3]==1:temp_set[(user,item)][step]=1

	real_train_set = []
	neg_count=0
	pos_count=0
	for samples in train_set:
		for sample in samples:
			if sample[-1]==1:pos_count+=1
			if sample[-1]==0:neg_count+=1
			real_train_set.append(sample)
			writer.writerow(sample)

	print "Sample Size: %s"%len(real_train_set)
	print "Negative Sample Size: %s"%neg_count
	print "Positive Sample Size: %s"%pos_count

	rfile.close()
	wfile.close()

def sampling(step,proportion):
	if not os.path.exists("train_data_%s.csv"%step):
		print "file of step %s not exists"%step
		return
	rfile=file("train_data_%s.csv"%step,"r")
	wfile=file("sample_data_%s_%s.csv"%(step,proportion),"w")

	reader=csv.reader(rfile)
	writer=csv.writer(wfile)

	pos_set=[]
	neg_set=[]

	for line in reader:
		if reader.line_num%10000==0:print reader.line_num
		line = [int(t) for t in line]
		if line[-1]==1:pos_set.append(line[:])
		if line[-1]==0:neg_set.append(line[:])

	print "Negative Sample Size: %s"%len(pos_set)
	print "Positive Sample Size: %s"%len(neg_set)

	print "N/P :%s"%(len(neg_set)/len(pos_set))

	neg_num =len(pos_set)*proportion

	neg_set = random.sample(neg_set,neg_num)

	sample_set = pos_set+neg_set
	random.shuffle(sample_set)

	for sample in sample_set:
		writer.writerow(sample)

	rfile.close()
	wfile.close()

def LR(fileName):
	data_set = np.loadtxt(fileName,delimiter=",")
	X = data_set[:,-4:-2]
	y = data_set[:,-1]

	X = preprocessing.scale(X)

	X_train,X_test,y_train,y_test = train_test_split(X,y,random_state=1)

	logRes = LogisticRegression(C=1,penalty="l1",tol=0.001)
	logRes.fit(X,y)

	print logRes.intercept_
	print logRes.coef_

	y_pred = logRes.predict(X_test)

	print np.sqrt(metrics.mean_squared_error(y_test,y_pred))

	return logRes














    


