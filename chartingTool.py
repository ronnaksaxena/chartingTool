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
'''
ticker = input('Enter Ticker Symbol:')
timeFrame = int(input('Enter Span of Chart in Days:'))
start = dt.datetime.now() - dt.timedelta(days=timeFrame)
end = dt.datetime.now()
'''
ticker = 'PFE'
start = dt.datetime(1999,11,1)
end = dt.datetime(2000,5,1)


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

#test with F chart from 12/1/1998-12/1/1999
#checks if trend is double top
def isDoubleTop(sma10):
    trend = 'up'
    patternStarted = False
    lastPrice = sma10[9]
    #local extrema tuples are (Min/Max, index)
    firstLMax = secondLMax = (-1, -1)
    firstLMin = (float('inf'), -1)
    for i in range(10,len(sma10),5):
        trend = 'up' if sma10[i] > lastPrice else 'down'
        lastPrice = sma10[i]
        if not patternStarted:
            #trying to find first local max/resistance
            if trend=='up':
                firstLMax = (sma10[i], i)
            #check for signs of pattern starting
            elif -1 < firstLMax[1]:
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
            elif trend=='down' and sma10[i] < firstLMin[0]:
                #meets pattern if breaks support
                return True
    return False

#test with PFE chart from 11/1/1999-05/1/200
#checks if trend is double bottom
def isDoubleBottom(sma10):
    trend = 'down'
    patternStarted = False
    lastPrice = sma10[9]
    #local extrema tuples are (Min/Max, index)
    firstLMin = secondLMin = (float('inf'), -1)
    firstLMax = (float('-inf'), -1)
    for i in range(14,len(sma10),5):
        trend = 'up' if sma10[i] > lastPrice else 'down'
        lastPrice = sma10[i]
        #trying to find firstLMin/support
        if not patternStarted:
            if trend=='down':
                firstLMin = (sma10[i], i)
            #check for signs of pattern starting
            elif firstLMin[1] > 0:
                patternStarted = True
                firstLMax = (sma10[i], i)
        #check if pattern meets requirements
        else:
            #try to find localMax/Resistance
            if trend=='up' and secondLMin[1]<0:
                firstLMax = (sma10[i], i)
            elif trend=='down':
                #checks if broke support too early then break pattern
                if sma10[i] < (firstLMin[0] * 0.9):
                    firstLMin = (float('inf'), -1)
                    secondLMin = (float('inf'), -1)
                    firstLMax = (float('-inf'), -1)
                    patternStarted = False
                else:
                    secondLMin = (sma10[i],i)

            #checks if second uptrend breaks resistance
            elif trend=='up' and sma10[i]>firstLMax[0]:
                #check if local mins are too far away
                print(firstLMin)
                print(firstLMax)
                print(secondLMin)
                if not (firstLMax[1] - firstLMin[1])*0.5 <= (secondLMin[1] - firstLMax[1]) <= (firstLMax[1] - firstLMin[1])*1.5:
                    firstLMin = (float('inf'), -1)
                    secondLMin = (float('inf'), -1)
                    firstLMax = (float('-inf'), -1)
                    patternStarted = False
                #found pattern
                else:
                    return True
    return False

                



            


print(isDoubleBottom(sma10))

#plots candlestick chart
mpf.plot(data, **kwargs,style=s)



        







