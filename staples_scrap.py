import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time 
import pandas as pd
df = pd.read_csv(r"D:\Scrapy\Office-Depot-Scrapper\Staples-SubCategories.csv")
df = df['SubCategories'].tolist()
# links=links[:500]
driver  = webdriver.Chrome(service =Service(ChromeDriverManager().install()))
for req in df:
    driver.get(req)