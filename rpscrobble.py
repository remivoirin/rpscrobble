#!/usr/env python
# Scrobble what's playing on Radio Paradise to your LastFM account.

# Imports #

from bs4 import BeautifulSoup
from datetime import datetime
from urllib2 import urlopen
import argparse
import pylast
import sys


# Global variables #

rpurl = "http://www.radioparadise.com/rp2-content.php"
rpseparator = u'\u2014'
songfilelocation = ".rpscrobble.tmp"
fileseparator = "|"
lastfmuser = ""
lastfmpass = ""
lastfmapikey = ""
lastfmapisecret = ""


# Functions #

# Write given artist and title to songfile
def dumpsongfilecontent(currartist, currtitle):
	songfile = None
	try:
		songfile = open(songfilelocation, "w+")
	except IOError as exc:
		print exc
		print "Can't open or create " + songfilelocation + ", exiting."
		exit(1)
	
	songfile.write(datetime.now().strftime('%s') + fileseparator + currartist + fileseparator + currtitle)	
	return None

# Return split content of songfile
def splitsongfilecontent(songfilecontent):
	contentarray = songfilecontent.split(fileseparator)
	return contentarray[0], contentarray[1], contentarray[2]

# Proceed to scrobble
def doscrobble(ts, artist, title):
	lastfmpasshash = pylast.md5(lastfmpass)
	lastfm_network = pylast.LastFMNetwork(api_key=lastfmapikey, api_secret=lastfmapisecret, username=lastfmuser, password_hash=lastfmpasshash)
	lastfm_network.scrobble(artist, title, ts)
	return None


# Main #

reload(sys)
sys.setdefaultencoding('utf8')

# Print help message if necessary
parser=argparse.ArgumentParser(
    description="Scrobble what's playing on Radio Paradise to your LastFM account.")
args=parser.parse_args()

# Get current song
rawrpcont = None
try:
	rawrpcont = urlopen(rpurl)
except URLerror as exc:
	print exc.reason

currsong = None
currartist = None
currtitle = None
try:
	parsablerpcont = BeautifulSoup(rawrpcont.read(), "html.parser")
	currsong = parsablerpcont.body.find_all('a', attrs={'class':'song_title'})[3].text
	currartist = currsong.partition(rpseparator)[0]
	currtitle = currsong.partition(rpseparator)[2]
except Exception as exc:
	print exc

# Try to read songfile content if it exists.
songfilecontent = None
try:
	with open(songfilelocation, "r") as songfile:
		songfilecontent = songfile.read()
		songfile.close()
except IOError as exc:
	pass

# Empty song file : write TS + track in songfile
if not songfilecontent:
	dumpsongfilecontent(currartist, currtitle)

else:
	# Not empty song file: let's check if it's changed.
	storedts, storedartist, storedtitle = splitsongfilecontent(songfilecontent)

	# Current song has changed: try scrobbling!
	# Can't know if half of the song was played, so make 120 seconds the only criteria.
	if currartist != storedartist or currtitle != storedtitle:
		dumpsongfilecontent(currartist, currtitle)
		if (int(datetime.now().strftime('%s')) - int(storedts)) > 120:
			doscrobble(storedts, storedartist, storedtitle)
