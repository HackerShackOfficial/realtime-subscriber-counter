# subscribercounter.py
import requests
import json
import sys
import argparse
import schedule
import time
import functools

# add command line arguments
parser = argparse.ArgumentParser(description='Realtime statistics counter')
parser.add_argument('--youtubeApiKey', dest='apiKey',
                   help='The API key for Youtube Data API')
parser.add_argument('--channelId', dest='channelId',
                   help='The ID for your youtube channel')
parser.add_argument('--crypto', dest='crypto',
                   help='The symbol for a cryptocurrency')

args = parser.parse_args()

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
				price = str(round(float(coin['price_usd']), 2))
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
	print ret


if __name__ == '__main__':
	if (args.crypto is not None):
		schedule.every(5).seconds.do(updateCounter, getCryptoPrice, args.crypto)
	elif (args.apiKey is not None and args.channelId is not None):
		schedule.every(5).seconds.do(updateCounter, getSubscribers, args.channelId, args.apiKey)
	else: # No arguments provided
		sys.exit(0);

	# Run the scheduler
	while True:
		schedule.run_pending()
		time.sleep(1)


