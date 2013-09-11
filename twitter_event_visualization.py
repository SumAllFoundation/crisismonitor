
#!/usr/local/bin/python python
def twitter_entities_mongodb_timestamp(dbname,host):
	#Returns timeseries of hashtags and mentions from given database in MongoDB with
	#the collection name tweets. 
	#Encoded
	#Define Python Lists
	men = []
	has = []
	url = []
	med = []

	#Using MongoDB
	connection = pymongo.MongoClient(host)
	print connection
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
			#datetime.utcfromtimestamp(tweet['timestamp']/1000)
			men.append([{'time': dateutil.parser.parse(tweet['created_at']),'mention': mention} for mention in mentions if mentions])
			has.append([{'time': dateutil.parser.parse(tweet['created_at']),'hashtag': hashtag} for hashtag in hashtags if hashtags])
			url.append([{'time': dateutil.parser.parse(tweet['created_at']),'url': u} for u in urls if urls])
			if 'media' in tweet['entities'].keys():
				med.append([{'time': dateutil.parser.parse(tweet['created_at']),'media':m} for m in media if media])
		else:
			print tweet['_id'], ' not retrieved'
	#Filter out the empty entries
	print 'Retrieval complete. Retrieved ', len(has), ' items'
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
	mts = mts.str.lower()
	hts = hts.str.lower()
	# uts = uts.str.lower()
	# #pts = pts.str.lower() #Do not lower case. Case sensitive
	return(mts,hts,uts,pts)

def twitter_top_entities_by_timeinterval(*dfs):
	#Retrieves top n items for each time interval.
	#KPI is the count of hashtags. 
	#inputDict contains the classifications and translations. 
	#time interval defines as a letter. e.g. 'D'
	#nitems specifies the top entities for a given time period. A list.
	#Break the entire time series into periods specified by time interval
	output = []
	periodlist = []
	time_interval = 'D'
	nitems = [10,10,3,1]
	#Search terms. 
	#search_terms = [a['term'] for a in inputList]
	#Create the list of dictionaries first with period information
	for n, df in enumerate(dfs):
		print 'creating', df.name, ' dictionary'
		#Cdlonvert to PeriodIndex
		dfperiod = df.to_period(time_interval)
		timeperiods = set(dfperiod.index.tolist())
		#Create a list of dates
		for timeperiod in timeperiods:
			periodlist.append(timeperiod.strftime('%'+time_interval))
	#With unique set of time periods. 
	for period in set(periodlist):
		output.append({'date': period})
	#Add to the list of dictionaries matching period information
	for n, df in enumerate(dfs):
		print 'adding to', df.name, ' dictionary'
		#Convert to PeriodIndex
		dfperiod = df.to_period(time_interval)
		timeperiods = set(dfperiod.index.tolist())
		#Create a list of Dictionaries with dates
		for timeperiod in timeperiods:
			#Date
			date = timeperiod.strftime('%'+time_interval)
			temp = dfperiod.ix[timeperiod].value_counts()[:nitems[n]]
			#Np.int64 not serializable. Switch to float to 
			temp = temp.astype(float)
			#Create temp lists to append to each dictionary
			metricList=[]
			#Loop to take care of each top item
			for ix, count in temp.iteritems():
				#Dictionary to append to metric list
				metricDict ={}
				#Adding title if URL to Picture Exists
				if df.name in 'url':
					metricDict = {df.name: ix, 'total': count, 'title': html_title_retrieve(ix)}
				elif df.name in 'hashtag':
				#Adding translation and category if hashtag is in input dictionary.
					#t = [i for i,x in enumerate(search_terms) if x in ix]
					#t = inputList[t[0]]
					print ix, ' found'
					metricDict = {df.name: ix, 'total': count}
				elif df.name in 'media':
					try:
						f = urllib2.urlopen(urllib2.Request(ix))
						deadLinkFound = False
					except:
						deadLinkFound = True
					if deadLinkFound is False:
						metricDict = {df.name: ix, 'total': count}
				else:
					#Else: If mention, broken media link or hashtag with no translatation or category
					metricDict = {df.name: ix, 'total': count}
				#Metric Appended for each top item. 
				metricList.append(metricDict)
			#Append to the dictionary list if date exists.
			for dic in output:
				if dic['date'] in date:
					dic[df.name] = metricList
					if df.name in 'hashtag':
						#Adding KPI dictionary. 
						dic['KPI'] = {df.name: len(dfperiod.ix[timeperiod])}
	return(output)

def html_title_retrieve(url):
    #Replace url links with titles where available
	#Append the urlList with url header if applicable. 
	try:
		f = urllib2.urlopen(url)
		data=f.read()
		f.close()
		soup = BeautifulSoup(data)
		header = soup.title.string
	except:
		header = ''
	return(header)

def tagging_events(tags_file_name,rawDict):
	#Import input file
	desc = []
	with open('%s.json' %(tags_file_name)) as f:
		for line in f:
			desc.append(json.loads(line))
	f.close()
	desc = desc[0]
	#Append events and EventKPIs
	events = desc['events']
	eventKPIs = desc['eventKPI']
	categories = desc['categories']
	#Event
	for event in events:
		date = event['date']
		for dic in rawDict:
			if dic['date'] in date:
				print 'events', date
				dic['event'] = {'desc': event['description']}
	#KPI
	for event in eventKPIs:
		date = event['date']
		for dic in rawDict:
			if dic['date'] in date:
				print 'eventKPIs', date
				dic['eventKPI'] = {'Casualties':event['Casualty'], 'Refugees': event['Registered Refugees']}
	#Category
	for category in categories:
		for dic in rawDict:
			for hashtag in dic['hashtag']:
				if hashtag['hashtag'] in category['term']:
					print hashtag['hashtag'], ' found'
					hashtag['category'] = category['category']
					hashtag['english'] = category['english']
	embeddedDict = rawDict
	return(embeddedDict)

if __name__ == "__main__":
	import sys, getopt
	import twitter
	import pymongo
	from pymongo import MongoClient
	import itertools
	from pandas import Series
	import dateutil 
	import datetime
	import json
	import pandas
	import numpy as np
	import time
	from pandas import DataFrame
	from bs4 import BeautifulSoup
	import urllib2
	#Retrieve the dataset from the database
	#Cut it into daily periods
	#Tag events 
	try:
		opts,args = getopt.getopt(sys.argv[1:],'d:i:o:h:', ['db=','input=','output=','host='])
	except getopt.GetoptError:
		pass
	#Parse Arguments
	for opt, arg in opts:
		if opt in ('-d', '--db'):
			db = arg
		elif opt in ('-i','--input'):
			tags_file_name = arg
		elif opt in ('-o','--output'):
			output_file_name = arg
		elif opt in ('-h','--host'):
			host = arg
	print db, tags_file_name, output_file_name, host
	#Create the JSON File
	[mts,hts,uts,pts] = twitter_entities_mongodb_timestamp(db,host)
	output	 =	twitter_top_entities_by_timeinterval(mts,hts,uts,pts)
	#If events are appended to input arguments
	embedded = tagging_events(tags_file_name,output)
	#Write raw file
	f = open('%s-raw.json' %(output_file_name),'w')
	f.write(json.dumps(embedded))
	f.close()
	####MANUPULATION OF VOLUME DATA##############
	#Estimation. Scales the numbers up using 09/05
	estimates = [{'date': '08/23/13', 'est': 20},
	{'date': '08/24/13', 'est': 21},
	{'date': '08/25/13', 'est': 21},
	{'date': '08/26/13', 'est': 29},
	{'date': '08/27/13', 'est': 65},
	{'date': '08/28/13', 'est': 89},
	{'date': '08/29/13', 'est': 86},
	{'date': '08/30/13', 'est': 89},
	{'date': '08/31/13', 'est': 100},
	{'date': '09/01/13', 'est': 79},
	{'date': '09/02/13', 'est': 57},
	{'date': '09/03/13', 'est': 29},
	{'date': '09/08/13', 'est': 50}]
	scale = int([entry['KPI']['hashtag']/67 for entry in embedded if entry['date'] in '09/05/13'][0])
	for estimate in estimates:
		for entry in embedded:
			if entry['date'] in estimate['date']:
				for h in entry['hashtag']:
					print entry['date'], h 
					print h['total'], ' before'
					temp= round(h['total'] / entry['KPI']['hashtag'] * estimate['est'] * scale)
					h['total'] = temp
					print h['total'], ' after'
				entry['KPI']['hashtag'] = round(estimate['est'] * scale)
	for entry in embedded:
		if entry['date'] in ['09/04/13','09/04/13','09/05/13','09/06/13','09/07/13','09/08/13','09/09/13']:
			for h in entry['hashtag']:
				h['total'] = h['total'] * 1.5
	###############################
	#Write to file
	f = open('%s.json' %(output_file_name),'w')
	f.write(json.dumps(embedded))
	f.close()
	print 'Output written to ', output_file_name

	for entry in embedded:
		for h in entry['hashtag']:
			temp= int(h['total'] / 2)
			h['total'] = temp



