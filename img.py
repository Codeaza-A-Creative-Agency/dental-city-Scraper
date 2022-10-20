import grequests
import pandas as pd
df= pd.read_csv(r'C:\scrapy\dentalcity\dental-city-Scraper\New-Dental-city-database.csv')
print(len(df))
df= df.drop_duplicates()

def resp():
    links =df['Product Page URL'].tolist()

    rs = (grequests.get(u) for u in links)
    respo= grequests.map(rs)
    
    return resp
