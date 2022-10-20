import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
url ='https://www.staples.com'
req= requests.get(url)
print(req.status_code)
bs = BeautifulSoup(req.content,'lxml')
cats= bs.findAll('a', target='flyout')
cat=[]
for anc in cats:
    print(url+anc.get('href'))
    cat.append(url+anc.get('href'))

    
print(len(cat))
