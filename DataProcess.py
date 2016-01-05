#coding=utf-8
import csv
import os
import math

#user_id,item_id,behavior_type,user_geohash,item_category,time
data_file = "data.csv"

def getUserid(td=0):
	rfile = file(data_file,"r")
	wfile = file("user_id.csv","w")

	reader = csv.reader(rfile)
	writer = csv.writer(wfile)

	user_buytime={}
	for line in reader:
		if reader.line_num%10000==0:print reader.line_num
		if reader.line_num==1:continue;
		if not user_buytime.has_key(line[0]):user_buytime[line[0]]=0
		if int(line[2])==4:user_buytime[line[0]]+=1

	count=0
	for it in user_buytime:
		if user_buytime[it]>td:
			writer.writerow([it])
			count+=1

	print "USER COUNT: "+str(count)

	rfile.close()
	wfile.close()

def getItemid():
	rfile = file(data_file,"r")
	wfile = file("item_id.csv","w")

	reader = csv.reader(rfile)
	writer = csv.writer(wfile)

	item_buytimes={}
	for line in reader:
		if reader.line_num%10000==0:print reader.line_num
		if reader.line_num==1:continue
		if not item_buytimes.has_key(line[1]):item_buytimes[line[1]]=0
		if int(line[2])==4:item_buytimes[line[1]]+=1

	count=0
	for it in item_buytimes:
		if item_buytimes[it]>0:
			writer.writerow([it])
			count+=1
	print "ITEM COUNT :"+str(count)

	rfile.close()
	wfile.close() 

def getCategory():
	rfile = file(data_file,"r")
	wfile = file("category_id.csv","w")

	reader = csv.reader(rfile)
	writer = csv.writer(wfile)

	category_set =set()
	for line in reader:
		if reader.line_num%10000==0:print reader.line_num
		if reader.line_num==1:continue
		category_set.add(line[4])

	print "category size:"+str(len(category_set))
	for it in category_set:writer.writerow([it])

	rfile.close()
	wfile.close()

def transformDate(month,day):
	if month==11:return day-17
	else:return day+13


def loadfile(filename):
	rfile = file(filename,"r")

	reader=csv.reader(rfile)
	content_list=[]
	for line in reader:
		if len(line)>1:content_list.append(line)
		else: content_list.append(line[0])

	rfile.close()
	return content_list

def dateCmp(x,y):
	if int(x[5])<int(y[5]):return -1
	elif int(x[5])>int(y[5]):return 1
	else:
		if x[6]<y[6]:return -1
		elif x[6]==y[6]:return 0
		else: return 1

def filegenerate(userid_file,itemid_file):
	if os.path.exists(userid_file):
		print userid_file+" existed"
	else:
		print userid_file+" not existed,getUserid"
		getUserid()

	if os.path.exists(itemid_file):
		print itemid_file+" existed"
	else:
		print itemid_file+" not existed,getItemid"
		getItemid()


def dataCleanAndTransform():
	userid_file = "user_id.csv"
	itemid_file = "item_id.csv"
	
	filegenerate(userid_file,itemid_file)

	user_list=set(loadfile(userid_file))
	item_list=set(loadfile(itemid_file))

	rfile = file(data_file,"r")
	wfile = file("cleaned_data.csv","w")

	reader = csv.reader(rfile)
	writer = csv.writer(wfile)
	count=0
	data_set=[]
	for user_id,item_id,behavior_type,user_geohash,item_category,time in reader:
		if reader.line_num%10000==0:print reader.line_num
		if reader.line_num==1:continue
		if user_id in user_list:
			date,hour = time.split(" ")
			year,month,day=date.split("-")
			newDate = transformDate(int(month),int(day))
			data_set.append([user_id,item_id,behavior_type,user_geohash,item_category,newDate,int(hour)])
			count+=1

	data_set.sort(dateCmp)
	writer.writerows(data_set)

	print "NEW DATA SIZE: %s"%count

	rfile.close()
	wfile.close()


def dataTransform():
    rfile = file("data.csv","r")
    wfile = file("tdata.csv","w")
     
    reader = csv.reader(rfile)
    writer = csv.writer(wfile)
     
    for user_id,item_id,behavior_type,user_geohash,item_category,time in reader:
        if reader.line_num%10000==0:print reader.line_num
        if reader.line_num==1:continue
        date,hour = time.split(" ")
        year,month,day=date.split("-")
        newDate = transformDate(int(month),int(day))
        writer.writerow([user_id,item_id,behavior_type,user_geohash,item_category,newDate,int(hour)])
		
    rfile.close()
    wfile.close()

def userBehaviorStat():
	rfile = file(data_file,"r")
	wfile = file("user_behavior_stat.csv","w")

	for user_id,item_id,behavior_type,user_geohash,item_category,time in reader:
		if reader.line_num%10000==0:print reader.line_num
		if reader.line_num==1:continue
		
	
	reader = csv.reader(rfile)
	writer = csv.writer(wfile)

def itemStat():
	rfile = file(data_file,"r")
	wfile = file("item_stat.csv","w")

	reader = csv.reader(rfile)
	writer = csv.writer(wfile)
	item_set = {}

	for user_id,item_id,behavior_type,user_geohash,item_category,time in reader:
		if reader.line_num%10000==0:print reader.line_num
		if reader.line_num>1:
			behavior_type=int(behavior_type)
			if not item_set.has_key(item_id):item_set[item_id]=[0,0]
	        if behavior_type==4:item_set[item_id][1]+=1
	        if behavior_type==3:item_set[item_id][0]+=1

	print len(item_set)
	i=0
	for item in item_set:
		if item_set[item][1]>0:i+=1
		if item_set[item][0]==0:item_set[item][0]=0.01
		writer.writerow([item,float(item_set[item][1])/item_set[item][0]])
	print i

	rfile.close()
	wfile.close()

def userStat():
	rfile = file("cleaned_data.csv","r")
	wfile = file("user_stat.csv","w")

	user_set={}

	reader = csv.reader(rfile)
	writer = csv.writer(wfile)

	for user_id,item_id,behavior_type,user_geohash,item_category,date,h in reader:
		if reader.line_num%10000==0:print reader.line_num
		if not user_set.has_key(user_id):user_set[user_id]=0
		if int(behavior_type)==4:user_set[user_id]+=1

	for user in user_set:
		writer.writerow([user,user_set[user]])

	rfile.close()
	wfile.close()

def getData(month,day):
	rfile = file("cleaned_data.csv","r")
	wfile = file("data_after_%s_%s.csv"%(month,day),"w")

	reader = csv.reader(rfile)
	writer = csv.writer(wfile)

	new_date = transformDate(month,day)

	for user_id,item_id,behavior_type,user_geohash,item_category,date,hour in reader:
		if reader.line_num%10000==0:print reader.line_num
		date = int(date)
		if date >= new_date:
			writer.writerow([user_id,item_id,behavior_type,user_geohash,item_category,date,hour])

	rfile.close()
	wfile.close()

def getEssentialData(td=0,month=12,day=12):
	getUserid(td)
	dataCleanAndTransform()
	getData(month,day)








