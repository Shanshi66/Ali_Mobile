import csv

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


