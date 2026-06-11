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

#loaded website using selenium
driver = webdriver.Chrome()
driver.get(url_current)
#establish waiting strategy to make sure entire page is loaded
#lazy scroll way(execute javascript to scroll)
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    #scroll to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(10)
    for i in range (4):
        driver.execute_script("window.scrollBy(0, -2000);")
        time.sleep(5)
        driver.execute_script("window.scrollBy(0,2000);")
    #check if more stuff loaded within the 10secs
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height


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
    #divs which have no repeating widths
    name = div.find("div", style=re.compile(widths["name"])).get_text(strip=True)
    print(name,i)
