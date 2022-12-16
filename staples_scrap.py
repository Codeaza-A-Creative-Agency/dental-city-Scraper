import scrapy 
from scrapy.crawler import CrawlerProcess
import pandas as pd

df = pd.read_csv(r"D:\Scrapy\Office-Depot-Scrapper\Staples-SubCategories.csv")
df = df['SubCategories'].tolist()
# links=links[:500]

class dental_city_scraper(scrapy.Spider):
    
    custom_settings = {
        'DOWNLOAD_DELAY' : 0.25,
        'RETRY_TIMES': 10,
        # export as CSV format
        'FEED_FORMAT' : 'csv',
        'FEED_URI' : 'New-Dental-city-data-with-category.csv',
    #     "ROTATING_PROXY_LIST" : ["108.59.14.208:13040", "108.59.14.203:13040"],
    #     "DOWNLOADER_MIDDLEWARES" : {
    #             "rotating_proxies.middlewares.RotatingProxyMiddleware" : 610,
    #             "rotating_proxies.middlewares.BanDetectionMiddleware" : 620}
    }
     
    name= 'scraper'
    
    def start_requests(self):
        for url in df:
            print(url[0])

            yield scrapy.Request(url=url, callback=self.parse)
    def parse(self,response):
        pass
 

process = CrawlerProcess()
process.crawl(dental_city_scraper)
process.start()