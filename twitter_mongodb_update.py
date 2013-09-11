#!/usr/local/bin/python python
def twitter_search_mongodb_update(dbname,search,oAuth,count,until):
	#Continously updates the collections in mongodb localhost given the search term.
	#Search term does not include hashtag.
	#oAuth is a dictionary containing twitter authorization keys. 
	import twitter
	import time
	import dateutil
	import calendar
	import pymongo
	import json
	#Using MongoDB
	connection = pymongo.MongoClient('mongodb://ec2-75-101-183-80.compute-1.amazonaws.com')
	dbtm = connection[dbname]
	tweets = dbtm.tweets
	#Connect to Twitter API
	t = twitter.Twitter(domain='api.twitter.com', api_version='1.1', auth=twitter.oauth.OAuth(oAuth['oauth_token'],oAuth['oauth_secret'],oAuth['consumer_key'],oAuth['consumer_secret']))
	#Loop to collect tweets. 
	#MongoDB
	while True:
		try:
			for term in search:
				term = '#'+term
				tw = t.search.tweets(count=count,q=term,show_user=True,until=until)
				statuses = tw['statuses']
				for status in statuses:
					try:	
						#Explicitly insert with id_str 
						status['_id'] = status['id_str']
						#Date - First to datetime, than to UNIX timestamp in miliseconds. 
						dt = dateutil.parser.parse(status['created_at'])
						uts = calendar.timegm(dt.utctimetuple())*1000
						status['timestamp'] = uts
						tweets.insert(status)
						print status['text'], status['created_at'], status['id_str']
					except:
						print status['id_str'], ' exists'
				#wait
				time.sleep(30)
		except:
			print 'Error. Prob Hit Rate Limit. Wait 10 minutes'
			time.sleep(600)

def twitter_stream_mongodb_update(dbname,search,oAuth,host):
	#Continously updates the collections in mongodb AWS given the search terms.
	#Search term does not include hashtag. Hashtag appended
	#oAuth is a dictionary containing twitter authorization keys. 
	import twitter
	import time
	import pymongo
	import json
	from dateutil import parser
	import calendar
	#Using MongoDB
	connection = pymongo.MongoClient(host)
	dbtm = connection[dbname]
	tweets = dbtm.tweets
	#Connect to Twitter Stream API
	twitter_stream = twitter.TwitterStream(auth=twitter.oauth.OAuth(oAuth['oauth_token'],oAuth['oauth_secret'],oAuth['consumer_key'],oAuth['consumer_secret']))
	#Append Hashtag, convert to string

	while True:
		try:
			#BUild the iterator
			iterator = twitter_stream.statuses.filter(track=search)
			#Insert into MongoDB
			for tweet in iterator:
				tweet['_id'] = tweet['id_str']
				#Date - First to datetime, than to UNIX timestamp in miliseconds. 
				dt = parser.parse(tweet['created_at'])
				uts = float(calendar.timegm(dt.utctimetuple())*1000)
				tweet['timestamp'] = uts
				try:
					tweets.insert(tweet)
					print tweet['text'], tweet['_id'], tweet['created_at']
				except:
					pass
		except:
			#wait
			print 'Reconnecting to Twitter stream'
			time.sleep(30)

