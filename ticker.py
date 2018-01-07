# ticker.py
import requests
import json
import sys
import argparse
import schedule
import time
import functools
import max7219.led as led
from max7219.font import proportional, TINY_FONT
from custom_font import CUSTOM_FONT

# add command line arguments
parser = argparse.ArgumentParser(description='Realtime statistics counter')
parser.add_argument('--youtubeApiKey', dest='apiKey',
                   help='The API key for Youtube Data API')
parser.add_argument('--channelId', dest='channelId',
                   help='The ID for your youtube channel')
parser.add_argument('--crypto', dest='crypto',
                   help='The symbol for a cryptocurrency')

parser.add_argument('--ticker', dest='ticker', action='store_true',
                   help='Show a crypto ticker')

args = parser.parse_args()

def getCryptoTickerPriceMap():
	cryptos = ['BTC', 'ETH', 'BCH', 'LTC', 'DOGE', 'DASH', 'XRP', 'ADA', 'XEM', 'XLM', 'MIOTA']
	ret = {};

	for c in cryptos:
		ret[c] = getCryptoPrice(c)

	return ret

def formatCryptoTicker(prev, current):
	ret = ''
	for key in current:
		if current[key] is not None:
			symbol = '\xfe'
			if key in prev:
				new = round(float(current[key]), 2)
				old = round(float(prev[key]), 2)
				if old > new:
					symbol = '\x1f'
				elif new > old:
					symbol = '\x1e'
			ret = ret + key + symbol + current[key] + ' '

	return ret

def getCryptoPrice(c):
	"""
	Fetches crypto currency prices. 
	If the specified currency does not exist, return None. Otherwise, return the price in USD. 

	API docs: https://coinmarketcap.com/api/
	"""

	try:
		symbol = c.upper()
		r = requests.get('https://api.coinmarketcap.com/v1/ticker/?convert=USD')
		data = json.loads(r.text)
		for coin in data:
			if (coin['symbol'] == symbol):
				price = "{0:.2f}".format(round(float(coin['price_usd']), 2))
				return price

		print "Cryptocurrency not found in response data"
		return None

	except Exception as e:
		print str(e)
		return None

def getSubscribers(channelId, apiKey):
	"""
	Fetches channel statistics. 
	Returns the Youtube subscriber count for the channel. Returns None if the call fails. 

	API docs: https://developers.google.com/youtube/v3/
	"""

	try:
		r = requests.get('https://www.googleapis.com/youtube/v3/channels?part=statistics&id=' + channelId + '&key=' + apiKey)
		subscriberCount = json.loads(r.text)["items"][0]["statistics"]["subscriberCount"]
		return subscriberCount
	except Exception as e:
		print str(e)
		return None

def updateCounter(job_func, *args, **kwargs):
	"""
	Updates the LED matrix with the current count. Values are fetched from the specified job func,
	"""

	ret = functools.partial(job_func, *args, **kwargs)()
	device.show_message(ret, font=proportional(TINY_FONT))


if __name__ == '__main__':
	device = led.matrix(cascaded = 4)
	device.orientation(90)
	if (args.crypto is not None):
		schedule.every(5).seconds.do(updateCounter, getCryptoPrice, args.crypto)
		
		# Run the scheduler
		while True:
			schedule.run_pending()
			time.sleep(1)

	elif (args.apiKey is not None and args.channelId is not None):
		schedule.every(5).seconds.do(updateCounter, getSubscribers, args.channelId, args.apiKey)

		# Run the scheduler
		while True:
			schedule.run_pending()
			time.sleep(1)

	elif (args.ticker is not None):

		oldPriceMap = {}
		while True:
			ret = getCryptoTickerPriceMap()
			msg = formatCryptoTicker(oldPriceMap, ret)
			device.show_message(msg + '   ', font=proportional(CUSTOM_FONT))
			if cmp(ret, oldPriceMap) != 0: # update the oldpricemap to retain diff symbols
				oldPriceMap = ret

	else: # No arguments provided
		sys.exit(0);

	


