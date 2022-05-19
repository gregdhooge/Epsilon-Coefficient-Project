#!/usr/bin/env python
# coding: utf-8

# In[10]:


''' 
This code takes the beta coefficient and prepares it for the integration of machine learning, specifically linear regression.
The beta coefficient assesses a stock's volitity with respect to the market
The formula comes from the covariance of the stock with respect to the market over the market variance
The cost function happens to be one half of the variance formula and that is modified in this code
The coefficient of in this code divides the covariance of 10 random stocks over the cost function
'''

import pandas as pd   
import pandas_datareader as web #Datareader will pull the stocks from Yahoo Finance
from datetime import date
import xlrd
import random

#Beginning and end dates of the simulation
start_date = date(2022,1,1)
end_date = date(2022,1,31)

def assess():
    
    
    Data = web.DataReader(['SPY'],'yahoo',start_date,end_date)['Adj Close']
    '''
    The market assessment is done through a S&P 500 ETF with a share price around a tenth of the index
    The volitility will remain the same throughout the data
    '''
    Market_unclean = Data.pct_change() #Takes percent change
    Market = Market_unclean.dropna() #Drops initial value
    
    distance = 0 - Market #Assesses volitility
    cost = sum(distance['SPY']**2)/(2*len(Market)) #Cost function
    print("The market is assessed at " + str(cost))
    
    # All stocks are listed in an Excel sheet and are drawns from this spreadsheet
    book = xlrd.open_workbook(r'C:\Users\gregd\OneDrive\Documents\The List of All Lists.xls')
    first_sheet = book.sheet_by_index(0)
    NASDAQ = (first_sheet.row_slice(rowx=0,
                                start_colx=1,
                                end_colx=7238))
    NYSE = (first_sheet.row_slice(rowx=8,
                                start_colx=1,
                                end_colx=2790))
    All = NASDAQ + NYSE
    
    #Randomly selects 10 stocks from the spreadsheet
    tickers = []
    while(len(tickers) != 10):
        tick = random.choice(All).value
        try:
            stock = web.DataReader(tick,'yahoo',start_date, end_date)['Adj Close']
            if(sum(stock)/len(stock) >= 8):
                tickers.append(tick)
        except:
            None
    print("The stocks to be assessed are:")
    print(tickers)   
    
    #Draws ticker prices from Yahoo and concatenates them into a dataframe for percent change analysis
    Assessments = web.DataReader(tickers,'yahoo', start_date, end_date)['Adj Close'] 
    df = Assessments.dropna(axis=1)
    Assessment = pd.concat([df], axis=1)
    pct_change_buy_NAN = Assessment.pct_change()
    pct_change = pct_change_buy_NAN.dropna() 
    
    
    for i in df.columns:
        cov_distance = 0 - pct_change[i] #Assess stock distance
        cov_sum = sum(cov_distance*distance['SPY'])/(len(pct_change) - 1) #Multiplies market distance and divides by n-1
        print("The covariance of " + str(i) + " is " + str(cov_sum)) 
        epsilon = cov_sum/cost #Divides covariance over cost function
        print("The coefficient is " + str(epsilon))
        print("---")
    
assess()

