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