#coding=utf-8
import csv
import os
import math

#user_id,item_id,behavior_type,user_geohash,item_category,time
data_file = "data.csv"

def getUserid():
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
		if user_buytime[it]>0:
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

def filegenerate():
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
		if user_id in user_list and item_id in item_list:
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


def userBehaviorStat():
	rfile = file(data_file,"r")
	wfile = file("user_behavior_stat.csv","w")

	

	reader = csv.reader(rfile)
	writer = csv.writer(wfile)



def getDataOnly34():
	rfile = file(tdata_file,"r")
	wfile = file("data34.csv","w")

	reader = csv.reader(rfile)
	writer = csv.writer(wfile)
	
	data_set=[]
	for line in reader:
		if line[2]=="3" or line[2]=="4":
			data_set.append(line)

	print len(data_set)

	data_set.sort(dateCmp)

	writer.writerows(data_set)

	rfile.close()
	wfile.close()






