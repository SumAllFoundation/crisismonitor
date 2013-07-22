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
	m = []
	h = []
	u = []

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
			#Build the list
			m.append([{'time': parser.parse(tweet['created_at']),'mention': mention} for mention in mentions if mentions])
			h.append([{'time': parser.parse(tweet['created_at']),'hashtag': hashtag} for hashtag in hashtags if hashtags])
			u.append([{'time': parser.parse(tweet['created_at']),'url': url} for url in urls if urls])
		else:
			print tweet['_id'], ' not retrieved'
	#Filter out the empty entries
	m = filter(None,m)
	h = filter(None,h)
	u = filter(None,u)
	#Collapse the list of dicts
	m = list(itertools.chain(*m))
	h = list(itertools.chain(*h))
	u = list(itertools.chain(*u))
	#DataFrame indexed to timestamps. 
	h = pandas.DataFrame.from_records(h)
	h.index=h.time
	hts=Series(h.hashtag,h.index)
	m = pandas.DataFrame.from_records(m)
	m.index = m.time
	mts=Series(m.mention,m.index)
	u = pandas.DataFrame.from_records(u)
	u.index =u.time
	uts = Series(u.url,u.index)
	#Lower case
	mts = mts.str.lower()
	hts = hts.str.lower()
	uts = uts.str.lower()
	return(mts,hts,uts)