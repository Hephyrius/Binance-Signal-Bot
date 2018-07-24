# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 19:39:49 2018

@author: Khera
"""

import time
import binance
from binance.client import Client
from binance.enums import *
from numpy import *
import math
import datetime
import CoreFunctions as cf
#%%

api_key = 'API_KEY'
api_secret = 'API_SECRET'
client = Client(api_key, api_secret)

#%%
firstRun = True
makeTrade = False

state = 0
prevTime = 0

data = []
signals = []

currentBtc = cf.getCoinBalance(client, 'btc')
print(currentBtc)
currentBnb = cf.getCoinBalance(client, 'bnb')
print(currentBnb)
currentTRX = cf.getCoinBalance(client, 'TRX')
print(currentTRX)

hasToken = False
currentTokenBalance = 0

#to change market just use the find and replace command to replace TRX with any other symbol.
#For example replace TRX with LRC for the LRC-BTC market
market = "TRXBTC"
trade = "TRX"
sellToBuyTransition = False

buyPrice = 0
bestPrice = 0
sinceBest = 0

while(True):
    
    #check time stamp if its different then add to list and change state
    #IMPORTANT 498 is the latest full candle. if we use 499 ie the last candle
    #we are using incomplete data which can cause false crossovers!
    if state == 0:
        
        candles = client.get_klines(symbol=market, interval=Client.KLINE_INTERVAL_5MINUTE)
        
        if firstRun == True:
            prevTime = datetime.datetime.fromtimestamp(candles[498][0]/ 1e3)
            
            firstRun = False
            makeTrade = True
            
            for i in range(499):
                data.append(candles[i])
            
        else:

            currTime = datetime.datetime.fromtimestamp(candles[498][0]/ 1e3)
            
            if prevTime != currTime:
                data.append(candles[498])
                prevTime = currTime
                makeTrade = True
                
            else:
                
                makeTrade = False
                
        print(makeTrade)
        
        # if timestamp is different then we attempt to trade
        if makeTrade == True:
            state = 1
            makeTrade = False
        #if its not then look for early selling opporunity to cash in profits
        else: 
            
            if hasToken == True:
                try:
                    
                    prices =  client.get_order_book(symbol=market)
                    price = prices['bids'][0][0]
                    
                    if float(price) > float(bestPrice):
                        
                        bestPrice = price
                        sinceBest = 0
                    else:
                        sinceBest = sinceBest + 1
                        
                    if (float(price)/float(buyPrice))>1.001 and sinceBest >= 2:
                        
                        print("Selling")                    
                        sellAmt = int(cf.getCoinBalance(client, trade))
                        
                        cf.executeSell(client, market, sellAmt)
                        currentTokenBalance = 0
                        hasToken = False
                        sellToBuyTransition = False
                        buyPrice = 0
                        bestPrice = 0
                        sinceBest = 0
                        currentBtc = cf.getCoinBalance(client, 'btc') 
                    else:
                        print("no early exit")
                        
                        
                except Exception as e:
                    print(e)
            
            
            time.sleep(10)
            
    #make signals data used for the strategy
    if state == 1:
        signals = cf.makeTrainingData(data)
        print(1)
        state = 2
    
    #buy BNB if we have less than required minimum - Uncomment in order to allow this to work!
    if state == 2:
        
#        currentBnb = cf.getCoinBalance(client, 'bnb')
#        
#        if currentBnb < 0.01:
#            cf.executeBuy(client, 'BNBBTC', 0.1)
        
        currentBtc = cf.getCoinBalance(client, 'btc') 
        state = 3
    
    #make trade based on calculated signals
    if state == 3:
        current = signals[len(signals)-1]
        
        if current[0] > current[1]:
            print("Buy Signal")
            
            if hasToken == False and sellToBuyTransition == True:
                try:
                    print("Buying")
                    currentBtc = cf.getCoinBalance(client, 'btc') 
                    
                    prices =  client.get_order_book(symbol=market)
                    price = prices['asks'][0][0]
                    buyPrice = price
                    buyAmt = int(currentBtc / float(price))
                    
                    cf.executeBuy(client, market, buyAmt)
                    currentTokenBalance = buyAmt
                    hasToken = True
                    
                    state = 0
                    time.sleep(10)
                    
                except Exception as e:
                    print(e)
            else:
                state = 0
                time.sleep(10)
            
        if current[0] < current[1]:
            print("Sell Signal")
            
            if sellToBuyTransition == False:
                sellToBuyTransition = True
                
            if hasToken == True:
                try:
                    print("Selling")                    
                    sellAmt = int(cf.getCoinBalance(client, trade))
                    
                    cf.executeSell(client, market, sellAmt)
                    currentTokenBalance = 0
                    hasToken = False
                    
                    currentBtc = cf.getCoinBalance(client, 'btc') 
                    state = 0
                    time.sleep(10)
                    
                except Exception as e:
                    print(e)
            else:
                state = 0
                time.sleep(10)
                
