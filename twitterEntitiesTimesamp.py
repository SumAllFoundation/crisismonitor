#!user/bin/env python
def twitterEntitiesTimestamp(dbname):
	#Returns timeseries of hashtags and mentions
	import twitter
	import time
	import couchdb
	import itertools
	import pandas
	from pandas import Series
	from dateutil import parser
	server = couchdb.Server()
	db = server[dbname]
	#Map Function CouchDB
	map_entities = 'function(doc){emit(doc._id,{created_at: doc.created_at, entities: doc.entities})}'
	#Entities 
	tweet_entities = [row.value for row in db.query(map_entities) if row.value]
	m = []
	h = []
	u = []
	for t in tweet_entities:
		hashtags = [hashtag['text'] for hashtag in t['entities']['hashtags']]
		mentions = [mentions['screen_name'] for mentions in t['entities']['user_mentions']]
		urls = [urls['expanded_url'] for urls in t['entities']['urls']]
		#Build the list
		m.append([{'time': parser.parse(t['created_at']),'mention': mention} for mention in mentions if mentions])
		h.append([{'time': parser.parse(t['created_at']),'hashtag': hashtag} for hashtag in hashtags if hashtags])
		u.append([{'time': parser.parse(t['created_at']),'url': url} for url in urls if urls])
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