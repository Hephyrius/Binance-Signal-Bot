# Binance-Signal-Bot
A Binance Bot that Trades Macd Crossovers 

# DISCLAIMER:

### This bot is intended to be a Proof-of-concept. The developer will not be responsible for Any losses that are made are as a result of using this tool. Understand the risks involved and Only invest amounts you are willing to lose.


## Suporting

If you appreciate my work send all crypto donations in Eth, Bnb, Matic, Avax etc on any chain to : 0xe0a09b49721FBD8B23c67a3a9fdE44be4412B8fD

## Structure

/CoreFunctions.py - Support functions, such as code to calc MACD, RSI ect
/TradingBoy.py - Core Bot Logics

## How it works:

This bot works by executing buy and sell trades, depending on whether or not a MACD crossover has occured on a cryptocurrency market. Be sure to read up on how MACD works and to look at the code in order to understand what is going on.

## Required Libraries

* python-binance
* numpy
* pandas <= 0.21

## How to use

Replace the API_KEY and API_SECRET with your own generated keypair for your account.

Change the market you want to trade on by either changing the referenced market manually OR replacing the current market(TRX) with find and replace. 


## Running in the background

in order to run the bot indefinetely in the background without logging on linux use:
```

nohup python3 & TradingBot.py

```

to use in the background in any console environment

```
python3 & TradingBot.py

```

## Does it make money?

Short answer Yes ... and No. In a bear market where the symbol is in a down trend, it tends to lose. In a bull market where the symbol is in a general up trend, it tends to win. The bot can run indefinetely if needed, I ran one bot for well over 10 days on an amazon EC2 instance in seoul.
