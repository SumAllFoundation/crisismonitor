#!user/bin/env python

def twitter_top_entities_timeseries(df,time_interval,nitems):
	#Retrieves top n items in TimeSeries and resizes the timeseries into time_interval. 
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

def twitter_top_entities_by_timeinterval(time_interval,nitems,*dfs):
	#Retrieves top n items for each time interval and 
	#[dic,count]=twitter_top_entities_by_timeinterval('D',10,hts,mts,uts,pts)
	import pandas
	import numpy as np
	import time
	from pandas import DataFrame
	count = {}
	dic={}
	#Break the entire time series into periods specified by time interval
	for df in dfs:
		print df.name
		#Convert to PeriodIndex
		dfperiod = df.to_period(time_interval)
		timeperiod = unique(dfperiod.index.tolist())
		#Create a List of Dictionaries
		diclist = []
		cntlist = []
		for interval in timeperiod:
			temp =   dfperiod.ix[interval].value_counts()[:nitems]
			#Np.int64 not serializable. Switch to float to 
			temp = temp.astype(float)
			#Dictionary of top items each timeperiod
			#Dictionary List
			diclist.append({interval.strftime('%D'): temp.to_dict()})
			#Append the dictionary list to dictionary
			dic[dfperiod.name]    = diclist
			#Total items each time period
			cntlist.append({interval.strftime('%D'): len(dfperiod.ix[interval])})
			#Append the dictionary list to dictionary
			count[dfperiod.name]  =  cntlist
	return(dic,count)

