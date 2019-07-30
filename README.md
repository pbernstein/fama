# What is this?

This project scrapes a variety of pricing and fundamental data about the us stock market.  

It uses that data to do regression analysis ( specifically, the fama french model ), attempts to predict pricing, then actively triggers trades in the market via the interactive brokers api.  It also publishes cleaned fundamental data about stocks in a timely manner.

This was something I tinkered with and ran as a hobby for a few years, and the "point" of the code base evolved as my interests changed. It was initally a loose collection of scripts but started to get a little more structure as I felt like adding it.   This was never really intended to be shared, but I've moved on in my life and this a fun discussion point to have with fellow data nerds.  

# Major capabilities of the code base

## Playing the stock market pricing data

The application uses the Fama French Model to predict stock prices.  

https://en.wikipedia.org/wiki/Fama%E2%80%93French_three-factor_model
https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html

This worked pretty well, and I got to a point where I could consistently get 5% - 10% better return than the market on an annual basis.  I got kind of bored with baby sitting it though and I don't have enough capital to live off of that return. Also, I came to the realization one day that I'm just not a gambler and that I want my impact on the world to be a bit broader than siphoning money out of the stock market.  Feel free to lift stuff directly, pull requests will be accepted :)

## Selling data

As a result of the work I had already done, I ended up with a lot of clean and current data that might be valuable.  I stood up a website on AWS and got all the feeds set up.  Fun times.  It published interesting events to a twitter account. All sorts of cool stuff.  However, I just couldn't get as excited about the marketing as the data work, and my day job got really fun and seemed like a better use of my time.  Again, feel free to steal!


# High level description:

Fair warning, none of this was ever meant to be public. In truth it was mostly a hobby to play with interesting and dirty data at a scale my home computing environment could support. As I alluded to above, I wrote all this years ago during a period after grad school while my day job was a bit boring. Apologies for poorly documented code or lack of best practices, unit tests, etc. 

## Languages

Pretty much everything is written in one of the following
- Python 2.7
- R 
- Shell

# Directories and what they are for: 

## scraping
- Scraping, parsing, and loading stock price data from the financial pages of google, yahoo as well as eod ( a paid data service ) 
## analysis
- Prepping the data, running the fama french regressions, playing with the co>efficients to see how it might better fit reality
## edgar, advfn
- Scraping, parsing, and loading stock fundamental ( filing ) data from https://www.advfn.com and https://www.sec.gov/edgar.shtml
## hist_plots
- Creating histograms out of the analysis results to try and find patterns to evaluate the different co-efficients
## trade
- the interface and code to actively trade against an Interactive Brokers account
## util
- common functions, database stuff, etc



# Requirements to run: 
- I put this together on ubuntu
- The trading (Interactive Brokers) stuff assumes you have a logged in client running 
- The eod stuff needs a login
- I used a mysql db underneath all of this
- Expected packages:
	sudo apt-get install python-mysqldb

# Where do I start?

## The best "entry" scripts for each directory are listed below.  

- scraping/daily_scrape.ksh
-- This script runs everyday, it scrapes a paid data service called EODData, and scrapes Yahoo and Google Finance. It pulls down pricing data for all stocks in NYSE, NASDAQ, and AMEX.  It loads the data to a mysql database. It scrubs and cleans the data. Then it cleans up after itself

- analysis/run_all.py
-- This script is a conveniant way to back test the model with a variety of different dollar amounts, regression co-efficents, time frames, etc, against the data. 

- edgar/pull_daily_xbrl.py
-- This pulls the most recent filings from the sec
-- There are other scripts in this directory that pull and load historical filings

- advfn/selenium_scrape.py
-- This pulls down historical filings

- advfn/load_advfn.py
-- This loads the files landed by the selenium_scrape.py script

- trade/execute.py
-- This scrapes the trade database and sees if there is any new trades to be initiated

# How did this run in production?


There are really two different 'production' environments. 

1) One that does the "builds" of the data, publishes the cleaned parsed data to wherever it needs to go, and publishes the next day's trade to the second production system.  
2) An AWS EC2 instance that watches and acts on the feed from the first production system. It also monitors all the positions that it currently has in the market and reverses them if certain criteria are met.



