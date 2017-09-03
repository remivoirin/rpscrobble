# RPScrobble
Small Python 2.7 script to scrobble / send to Last.FM what's playing on Radio Paradise (www.radioparadise.com).

## Requirements

* BeautifulSoup
```sh
pip install beautifulsoup4
```
More info at https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup

* PyLast
```sh
pip install pylast
```

## Setup

* Create a Last.FM API key and secret at https://www.last.fm/api/account/create.

* Put your API data and credentials in the global variables.
```python
lastfmuser = ""
lastfmpass = ""
lastfmapikey = ""
lastfmapisecret = ""
```

## Usage

For now, it's best to loop and execute the script every 60 seconds.
```sh
while : ; do python rpscrobble.py ; sleep 60 ; done
```

## Known limitations and things to do

* Daemonize
* Add proper logging
* Delete songfile (.rpscrobble.tmp) on exit

## Misc

If you have any request, please contact me at remi _at_ lags.is or @LagWire on Twitter.
Also, support Radio Paradise!

## License
MIT. See the LICENSE file for details.
