#!user/bin/env python


def twitter_search_mongodb_update(dbname,search,oAuth):
	#Continously updates the collections in mongodb localhost given the search term. 
	#oAuth is a dictionary containing twitter authorization keys. ß 
	import twitter
	import time
	import pymongo
	import json
	#Using MongoDB
	connection = pymongo.MongoClient("mongodb://localhost")
	dbtm = connection.turkeymonitor
	tweets = dbtm.tweets
	#Connect to Twitter API
	t = twitter.Twitter(domain='api.twitter.com', api_version='1.1', auth=twitter.oauth.OAuth(oAuth['oauth_token'],oAuth['oauth_secret'],oAuth['consumer_key'],oAuth['consumer_secret']))
	#Loop to collect tweets. 
	#MongoDB
	while True:
		try:
			for term in search:
				tw = t.search.tweets(count=100,q=term[0],show_user=True)
				statuses = tw['statuses']
				for status in statuses:
					try:	
						#Explicitly insert with id_str 
						status['_id'] = status['id_str']
						tweets.insert(status)
						print status['text']
					except:
						print status['id_str'], ' exists'
				#wait
				time.sleep(30)
		except:
			print 'Error. Prob Hit Rate Limit. Wait 10 minutes'
			time.sleep(600)