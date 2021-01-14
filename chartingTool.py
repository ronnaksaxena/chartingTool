import datetime as dt
import pandas_datareader as web
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt

#Code for plotting data from csv file
'''
SPX = pd.read_csv('^GSPC.csv')
#last 365 days
SPX = SPX.tail(365)

#sets dates as index
SPX.iloc[:,0] = pd.to_datetime(SPX.iloc[:,0], format = '%Y-%m-%d')
SPX = SPX.set_index(pd.DatetimeIndex(SPX['Date']))
'''

ticker = input('Enter Ticker Symbol:')
timeFrame = int(input('Enter Span of Chart in Days:'))
start = dt.datetime.now() - dt.timedelta(days=timeFrame)
end = dt.datetime.now()


#gets data and restructures it
data = web.DataReader(ticker, 'yahoo', start, end)
data = data[['Open','High','Low','Close','Adj Close','Volume']]
data.reset_index(inplace=True)
data = data.set_index(data['Date'])

#design for candlestick chart
kwargs = dict(type='candle',mav=(5),volume=False,title='{} Stock Price'.format(ticker))
mc = mpf.make_marketcolors(up='g',down='r')
s  = mpf.make_mpf_style(marketcolors=mc)

#plots candlestick chart
mpf.plot(data, **kwargs,style=s)

#get list of moving average values
sma5 = list(data['Close'].rolling(5).mean())



