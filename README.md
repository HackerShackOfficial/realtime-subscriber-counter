# Realtime Subscriber Counter / Cryptocurrency Ticker
An LED Matrix that counts subscribers (and cryptocurrency prices) in realtime.

Watch the video about how to make it [here](https://youtu.be/HN2RRBSAsn8).

See more instructions about how to make it on [hackster.io](https://www.hackster.io/hackerhouse/realtime-cryptocurrency-ticker-youtube-subscriber-counter-0ac8c5).

## Pre-requisites
+ Python 2.7
+ pip
+ Raspbian

## Wiring

| Board Pin	| Name	| Remarks	|RPi Pin |	RPi Function
|-----|------|------| -----|-----|
|1	|VCC	|+5V Power	|2	|5V0
|2	|GND	|Ground	|6	|GND
|3	|DIN	|Data In	|19	|GPIO 10 (MOSI)
|4	|CS	|Chip Select	|24	|GPIO 8 (SPI CE0)
|5	|CLK	|Clock	|23	|GPIO 11 (SPI CLK)

## Install Dependencies 

Before you run the program, make sure to install dependencies. Navigate to the project directory and run

```
pip install -r requirements.txt
```

to install the python dependencies. 

Enable the SPI driver for the max7219 LED module to work properly.

```
sudo raspi-config
```

Scroll down to `Advanced Options` (`Interfacing Options` on the Pi Zero) and press enter.

Scroll down to `SPI`, press enter, and select `yes`.

Reboot.

## Running the Program

The `ticker.py` program runs in three different modes: live subscriber counter, live cryptocurrency price, and cryptocurrency ticker. 

### Live Subscriber Counter

To run the program in live subscriber mode, you can run the program with the following arguments:

```
python ticker.py --youtubeApiKey API_KEY --channelId CHANNEL_ID
```

Where `CHANNEL_ID` is replaced with the channel ID from your youtube channel URL. (For instance Hacker House has the channel ID `UCEcNXmr7DYq1XxpWHSxaN0w` from https://www.youtube.com/channel/UCEcNXmr7DYq1XxpWHSxaN0w) and `API_KEY` is replaced with an API key from the Youtube Data API. 

You can obtain an API key for the Youtube Data API by visiting the [Google developer console](https://console.developers.google.com/apis).  Search for "Youtube Data API" and enable the API. Once the API has been enabled, visit the API settings page and click `credentials` in the left rail. On the credentials page, click `Create credentials` and select `API Key`.

### Cryptocurrency Price

You can also display the price of your favorite cryptocurrency by using the following arguments:

```
python ticker.py --crypto ETH
```

Where `ETH` can be replaced with your favorite cryptocurrency symbol. You can obtain the symbol for your cryptocurrency by searching https://coinmarketcap.com/ for it.

### Cryptocurrency Ticker

To run the LED bar in Cryptocurrency ticker mode, use the following arguments:

```
python ticker.py --ticker
```

By default, it shows the prices for a list of 11 cryptocurrencies. You can add more by modifying the `cryptos` variable in `ticker.py` [here](https://github.com/HackerHouseYT/realtime-subscriber-counter/blob/aae8f41e45a45a8098aa5c6d96be084bf0e504a5/ticker.py#L28). Simply add your symbols to the end of the list.

## Running on Startup

To run the program on startup, open your `rc.local` file with Vim.

```
sudo vim /etc/rc.local
```

Press `i` to edit, scroll to the line before `exit 0` and add

```
python /full/path/to/ticker.py --ticker
```

(Or add other options) and press `esc` then `ZZ` to save and exit.
