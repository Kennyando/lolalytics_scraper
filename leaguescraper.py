import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
#need html5,bs4,lxml,requests,pandas,numpy for webscraping,selenium,webdriver

url_current = 'https://lolalytics.com/lol/tierlist/'
url_16_10 = 'https://lolalytics.com/lol/tierlist/?patch=16.10'
url_16_09 = 'https://lolalytics.com/lol/tierlist/?patch=16.9'

full_data = []

#loaded website using selenium
driver = webdriver.Chrome()
driver.get(url_current)
#establish waiting strategy to make sure entire page is loaded
#lazy scroll way(execute javascript to scroll)
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    #tried implementing sleep after each scroll but found that just no sleep but gradual scroll like a human will load everything
    driver.execute_script("window.scrollBy(0, 500);")
    #innerHeight for visible webpage length, scrollY for how much has been scrolled, document.body.scrollHeight for entire height of webpage including not loaded content
    at_bottom = driver.execute_script("""
        return (window.innerHeight + window.scrollY) >= document.body.scrollHeight
    """)
    if at_bottom:
        break
#render html
lolalytics_html = driver.page_source
#exit selenium
driver.quit()

soup = BeautifulSoup(lolalytics_html,"html.parser")
individual_champs = soup.select("div[class *= 'flex h-[52px] justify-between text-[13px]']")

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

#iterate through info to extract each data wanted
for i,div in enumerate(individual_champs):
    #target each stat which have a different pixel width and choose accordingly the one which I want
    #name and games both have unique widths so no need to index into the correct one after finding all
    name = div.find("div", style=re.compile(widths["name"])).get_text(strip=True)
    games = div.find("div", style=re.compile(widths["games"])).get_text(strip=True)
    #will output all the divs, index first then strip after
    forty_px = div.find_all("div", style=re.compile(widths["tier"]))
    fortyeight_px = div.find_all("div", style=re.compile(widths["winrate"]))

    full_data.append({
        "name": name,
        "tier": forty_px[1].get_text(strip=True),
        "lane_pickrate": forty_px[2].get_text(strip=True),
        "winrate": fortyeight_px[0].get_text(strip=True),
        "pickrate": fortyeight_px[1].get_text(strip=True),
        "banrate":fortyeight_px[2].get_text(strip=True),
        "PBI": fortyeight_px[3].get_text(strip=True),
        "games": games
    })

all_champs_df = pd.DataFrame(full_data)
print(all_champs_df)
