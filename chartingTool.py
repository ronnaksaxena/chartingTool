import datetime as dt
import pandas_datareader as web
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mplfinance as mpf

#Define Time Frame (change to a year ago)

start = dt.datetime(2020,1,1)
end = dt.datetime.now()

#Load Data
ticker = 'AAPL' #str(input('Enter Ticker:'))
data = web.DataReader(ticker, 'yahoo', start, end)

# Restructures data
data = data[['Open','High','Low','Close']]
data.reset_index(inplace=True)
data['Date'] = data['Date'].map(mdates.date2num)

# Visualization
ax = plt.subplot()
ax.grid(True)
ax.set_axisbelow(True)
ax.set_title('{} Share Price'.format(ticker), color='white')
ax.set_facecolor('black')
ax.figure.set_facecolor('#121212')
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')
ax.xaxis_date()
'''candlestick_ohlc(ax, data.values, width=0.5, colorup='g')'''
mpf.plot(data.values)
#plt.show()

