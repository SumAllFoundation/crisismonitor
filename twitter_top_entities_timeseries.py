#!user/bin/env python
def twitter_top_entities_by_timeinterval(inputDict,time_interval,nitems,*dfs):
	#Retrieves top n items for each time interval.
	#KPI is the count of hashtags. 
	#inputDict contains the classifications and translations. 
	#time interval defines as a letter. e.g. 'D'
	#nitems specifies the top entities for a given time period. A list.
	import pandas
	import numpy as np
	import time
	from pandas import DataFrame
	from bs4 import BeautifulSoup
	import urllib2
	#Break the entire time series into periods specified by time interval
	diclist = []
	periodlist = []
	#Create the list of dictionaries first with period information
	for n, df in enumerate(dfs):
		print 'creating', df.name, ' dictionary'
		#Cdlonvert to PeriodIndex
		dfperiod = df.to_period(time_interval)
		timeperiods = set(dfperiod.index.tolist())
		#Create a list of dates
		for timeperiod in timeperiods:
			periodlist.append(timeperiod.strftime('%D'))
	#With unique set of time periods. 
	for period in set(periodlist):
		diclist.append({'date': period})
	#Add to the list of dictionaries matching period information
	for n, df in enumerate(dfs):
		print 'adding to', df.name, ' dictionary'
		#Convert to PeriodIndex
		dfperiod = df.to_period(time_interval)
		timeperiods = set(dfperiod.index.tolist())
		#Create a list of Dictionaries with dates
		for timeperiod in timeperiods:
			#Date
			date = timeperiod.strftime('%D')
			temp = dfperiod.ix[timeperiod].value_counts()[:nitems[n]]
			#Np.int64 not serializable. Switch to float to 
			temp = temp.astype(float)
			#Create temp lists to append to each dictionary
			metricList=[]
			#Loop to take care of each top item
			for ix, count in temp.iteritems():
				#Dictionary to append to metric list
				metricDict ={}
				#Adding title if URL
				if df.name in 'url':	
					metricDict = {df.name: ix, 'total': count, 'title': html_title_retrieve(ix)}
				elif df.name in 'hashtag' and  ix in inputDict.keys():
				#Adding translation and category if hashtag is in input dictionary
					print ix, ' found'
					metricDict = {df.name: ix, 'total': count ,'category': inputDict[ix]['category'],'english': inputDict[ix]['english']}
				else:
					print ix, ' not found'
					metricDict = {df.name: ix, 'total': count}
				#Metric Appended for each top item. 
				metricList.append(metricDict)
			#Append to the dictionary list if date exists.
			for dic in diclist:
				if dic['date'] in date:
					dic[df.name] = metricList
					if df.name in 'hashtag':
						#Adding KPI dictionary. 
						dic['KPI'] = {df.name: len(dfperiod.ix[timeperiod])}
	return(diclist)


def html_title_retrieve(url):
    #Replace url links with titles where available
	from bs4 import BeautifulSoup
	import urllib2
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



def twitter_top_entities_timeseries(df,time_interval,nitems):
	#Retrieves top n items across the entire timeline and resizes the timeseries into time_interval. 
	#mentions = twitter_top_entities_timeseries(mts,'H',20)
	#hashtags = twitter_top_entities_timeseries(hts,'H',20)
	import pandas
	import numpy as np
	import time
	from pandas import DataFrame
	#Top Entities to retrieve
	items = df.value_counts()
	items = items[:nitems]
	#Create Time Series
	ts = DataFrame(np.zeros((len(df),len(items))),columns=items.keys(),index=df.index)
	#Populative Time Series for nitems trending entities. 
	for item in items.keys():
		tmp = df.str.contains(item, na=False).values
		ts[item] = np.array(tmp, dtype=int)
	#Convert into Hourly
	tsh = ts.resample(time_interval, how='sum')
	#For MongoDB: Convert dtype to float
	tsh = tsh.astype(float)
	return(tsh)




