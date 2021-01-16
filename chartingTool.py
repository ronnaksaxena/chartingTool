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
kwargs = dict(type='candle',mav=(10),volume=False,title='{} Stock Price'.format(ticker))
mc = mpf.make_marketcolors(up='g',down='r')
s  = mpf.make_mpf_style(marketcolors=mc)


#get list of moving average values
sma10 = list(data['Close'].rolling(10).mean())

#checks if trend is double top
def isDoubleTop(sma10):
    trend = 'up'
    patternStarted = False
    lastPrice = sma10[4]
    #local extrema tuples are (Min/Max, index)
    firstLMax = secondLMax = (-1, -1)
    firstLMin = (float('inf'), -1)
    for i in range(5,len(sma10),7):
        trend = 'up' if sma10[i] > lastPrice else 'down'
        lastPrice = sma10[i]
        if not patternStarted:
            #trying to find first local max/resistance
            if trend=='up':
                firstLMax = (sma10[i], i)
            #check for signs of pattern starting
            if trend=='down' and -1 < firstLMax[1]:
                patternStarted = True
                firstLMin = (sma10[i], i)
        #check if pattern meets requirements
        else:
            #trying to find first local min/support
            if trend=='down' and secondLMax[1]<0:
                firstLMin = (sma10[i], i)
            elif trend=='up':
                #checks if broke resistance too early then break pattern
                if sma10[i]*1.10 > (firstLMax[0]):
                    firstLMax = secondLMax = (-1, -1)
                    firstLMin = (float('inf'), -1)
                    patternStarted = False
                else:
                    secondLMax = (sma10[i], i)
            elif trend=='down' and secondLMax[1]>0:
                #meets pattern if breaks support
                if sma10[i] < firstLMin[0]:
                    return True
    return False


#plots candlestick chart
mpf.plot(data, **kwargs,style=s)



        







