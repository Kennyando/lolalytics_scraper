import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

#need html5,bs4,lxml,requests,pandas,numpy for webscraping,selenium,webdriver

url_current = 'https://lolalytics.com/lol/tierlist/'
url_16_10 = 'https://lolalytics.com/lol/tierlist/?patch=16.10'
url_16_09 = 'https://lolalytics.com/lol/tierlist/?patch=16.9'

#loaded website using selenium
driver = webdriver.Chrome()
driver.get(url_current)
#establish waiting strategy to make sure entire page is loaded
WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.TAG_NAME, "body"))
)
#render html
lolalytics_html = driver.page_source
#exit selenium
driver.quit()

soup = BeautifulSoup(lolalytics_html,"html.parser")
individual_champs = soup.select("div[class *= 'flex h-[52px] justify-between text-[13px]']")

print(individual_champs)
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

#key 2 to key 13, each key represents a set data,champ name,rank,wr,pick,ban rate
    #for i in range(2,10):
        #champ_stats = div.find("div", attrs={"q:key": f"{i}"})
        #print(champ_stats.text)
for div in individual_champs:
    #divs which have no repeating widths
    name = div.find("div", style=re.compile(widths["name"])).get_text(strip=True)
