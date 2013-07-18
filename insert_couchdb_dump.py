#Dump
#$ curl -X GET http://localhost:5984/gezi/_all_docs?include_docs=true >
#ßgezidump.txt
#python
import json
import pymongo
from pymongo import MongoClient
count=0
client = MongoClient()
db = client.turkeymonitor
tweets = db.tweets
f = open('batch.json','r')
q = f.readlines()
for line in q:
	try:
		line = line.rstrip("\,\r\n")
		d = dict(json.loads(line))
		tweets.insert(d['doc'])
		count +=1
	except:
		print d['doc']['_id'],'not inserted'

print count + ' inserted'

hList=[]
for line in q:
	try:
		line = line.rstrip("\,\r\n")
		d = dict(json.loads(line))
		hashtags = d['doc']['entities']['hashtags']
		z = [hashtag['text'] for hashtag in hashtags]
		if u'dirençözüm' in z:
			print z
		hList.append(z)
		count += 1
		print count
	except:
		print 'cont'
hList = list(itertools.chain(*hList))