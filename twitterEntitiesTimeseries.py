#!user/bin/env python

#[mentions] = twitterEntitiesTimeseries(mts,'H',20)
#[hashtags] = twitterEntitiesTimeseries(hts,'H',20)
def twitterEntitiesTimeseries(df,time_interval,nitems):
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
	return(tsh)