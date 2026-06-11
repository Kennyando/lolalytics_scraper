import numpy as np
import pandas as pd
import requests
import lxml
from bs4 import BeautifulSoup
import re
#need html5,bs4,lxml,requests,pandas,numpy for webscraping

url_16_11 = 'https://lolalytics.com/lol/tierlist/'
url_16_10 = 'https://lolalytics.com/lol/tierlist/?patch=16.10'
url_16_09 = 'https://lolalytics.com/lol/tierlist/?patch=16.9'

#webpage is loaded dynamically need a ghost loading like selenium to load the whole page before we parse
webpage = requests.get(url_16_11)
soup = BeautifulSoup(webpage.content,"html.parser")

# isn't sorted by table tag but rather a big div container
# div class ="menu relative"
# each champion is under a flex h-[52px] div as well
#mapping out px lengths so can plug into BS to find
widths = {
    "name": "110px",
    "tier": "40px",
    "lane_pickrate": "40px",
    "winrate": "48px",
    "pickrate": "48px",
    "banrate": "48px",
    "PBI": "48px",
    "games": "72px"
}
#search via css selector
champ_divs = soup.select("div[class *= 'menu:left-[30px]']")
individual_champs = soup.select("div[class *= 'flex h-[52px] justify-between text-[13px]']")
print(individual_champs)
#key 2 to key 13, each key represents a set data,champ name,rank,wr,pick,ban rate
    #for i in range(2,10):
        #champ_stats = div.find("div", attrs={"q:key": f"{i}"})
        #print(champ_stats.text)
for div in individual_champs:
    #divs which have no repeating widths
    name = div.find("div", style=re.compile(widths["name"])).get_text(strip=True)
