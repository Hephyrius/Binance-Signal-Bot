"""
@author: Khera
"""

import time
from binance.client import Client
import csv
import pandas as pd 
import numpy as np

def emaPoints(data, dataPoints):
    ema1 = []
    
    for i in range(len(data)):
        ema = 0
        if i > 0:
            prevEma = ema1[i-1]
            multiplyer = 2/(dataPoints+1)
            ema = (float(data[i][4]) - prevEma)*multiplyer+prevEma

        ema1.append(ema)
    return ema1
#%%
def emaPointsMacd(data, dataPoints):
    ema1 = []
    
    for i in range(len(data)):
        ema = 0
        if i > 0:
            prevEma = ema1[i-1]
            multiplyer = 2/(dataPoints+1)
            ema = (data[i] - prevEma)*multiplyer+prevEma

        ema1.append(ema)
    return ema1

def macd(data):

    ema12 = emaPoints(data,12)
    ema26 = emaPoints(data,26)
    macd = []
    for i in range(len(ema12)):
        m = ema12[i]-ema26[i]
        macd.append(m)
    
    signal = emaPointsMacd(macd,9) 
    
    return macd, signal
#%%
def makeTrainingData(data):
    
    macda, signal = macd(data)
    
    features = []
    
    for i in range(100,len(data)):
        
        #x = [macda[i], signal[i]]
        x = [macda[i], signal[i]]
        features.append(x)
    return features

def getCoinBalance(client, currency):
    balance = float(client.get_asset_balance(asset=currency)['free'])
    return balance

def calculateRsi(data):
    
    RSI_N = 14
    RSI_THRESHOLD = 8
    closings = np.asarray(data, dtype=np.float)[-RSI_N - 1:, 4]
    diffs = np.diff(closings)
    ups = diffs.clip(min=0)
    downs = diffs.clip(max=0)
    ups_avg = pd.ewma(ups, span=RSI_N)[-1]
    downs_avg = -pd.ewma(downs, span=RSI_N)[-1]
    rs = ups_avg / downs_avg
    rsi = 100 - 100 / (1 + rs)
    return rsi
    
def executeBuy(client, market, qtyBuy):
    
    order = client.order_market_buy(symbol=market,quantity=qtyBuy)

def executeSell(client, market, qtySell):

    order = client.order_market_sell(symbol=market, quantity=qtySell)
    
