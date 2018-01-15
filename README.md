# realtime-subscriber-counter
An LED Matrix that counts subscribers (and cryptocurrency prices) in realtime.

## Pre-requisites
+ Python 2.7
+ pip
+ Raspbian

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

The `ticker.py` program runs in three different modes: live subscriber counter, live cryptocurrecy price, and cryptocurrecy ticker. 

### Live Subscriber Counter

To run the program in live subscriber mode, you can run the program with the following arguments:

```
python ticker.py --youtubeApiKey API_KEY --channelId CHANNEL_ID
```

Where `CHANNEL_ID` is replaced with the channel ID from your youtube channel URL. (For instance Hacker House has the channel ID UCEcNXmr7DYq1XxpWHSxaN0w from https://www.youtube.com/channel/UCEcNXmr7DYq1XxpWHSxaN0w) and `API_KEY` is replaced with an API key from the Youtube Data API. 

You can obtain an API key for the Youtube Data API by visiting the [Google developer console](https://console.developers.google.com/apis) Search for "Youtube Data API" and enable the API. Once the API has been enabled, visit the API settings page and click `credentials` in the left rail. On the credentials page, click `Create credentials` and select `API Key`.

### Cryptocurrency Price

### Cryptocurrency Ticker

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
