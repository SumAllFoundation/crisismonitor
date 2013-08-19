#!/usr/local/bin/python python
def twitter_entities_mongodb_timestamp(dbname):
	#Returns timeseries of hashtags and mentions from given database in MongoDB with
	#the collection name tweets. 
	#Encoded
	import twitter
	import time
	import pymongo
	from pymongo import MongoClient
	import itertools
	import pandas
	from pandas import Series
	from dateutil import parser

	#Define Python Lists
	men = []
	has = []
	url = []
	med = []

	#Using MongoDB
	connection = MongoClient("mongodb://localhost")
	db= connection[dbname]
	tweets = db.tweets
	#Go through the tweets collection. 
	for tweet in tweets.find():
		#{'entities': tweet['entities'],'created_at': tweet['created_at']}#
		if 'entities' in tweet.keys():
			hashtags = [hashtag['text'] for hashtag in tweet['entities']['hashtags']]
			mentions = [mentions['screen_name'] for mentions in tweet['entities']['user_mentions']]
			urls = [urls['expanded_url'] for urls in tweet['entities']['urls']]
			if 'media' in tweet['entities'].keys():
				media  = [media['media_url'] for media in tweet['entities']['media'] ]
			#Build the list
			men.append([{'time': parser.parse(tweet['created_at']),'mention': mention} for mention in mentions if mentions])
			has.append([{'time': parser.parse(tweet['created_at']),'hashtag': hashtag} for hashtag in hashtags if hashtags])
			url.append([{'time': parser.parse(tweet['created_at']),'url': u} for u in urls if urls])
			med.append([{'time': parser.parse(tweet['created_at']),'media':m} for m in media if media])
		else:
			print tweet['_id'], ' not retrieved'
	#Filter out the empty entries
	men = filter(None,men)
	has = filter(None,has)
	url = filter(None,url)
	med = filter(None,med)
	#Collapse the list of dicts
	men = list(itertools.chain(*men))
	has = list(itertools.chain(*has))
	url = list(itertools.chain(*url))
	med = list(itertools.chain(*med))
	#DataFrame indexed to timestamps. 
	has = pandas.DataFrame.from_records(has)
	has.index=has.time
	hts=Series(has.hashtag,has.index)
	men = pandas.DataFrame.from_records(men)
	men.index = men.time
	mts=Series(men.mention,men.index)
	url = pandas.DataFrame.from_records(url)
	url.index =url.time
	uts = Series(url.url,url.index)
	med = pandas.DataFrame.from_records(med)
	med.index =med.time
	pts = Series(med.media,med.index)
	#Lower case
	#mts = mts.str.lower()
	#hts = hts.str.lower()
	# uts = uts.str.lower()
	# #pts = pts.str.lower() #Do not lower case. Case sensitive
	return(mts,hts,uts,pts)