import scrapy 
from scrapy.crawler import CrawlerProcess
import pandas as pd
import re
df=pd.read_csv(r'C:\Users\PC\Staples-Categories.csv')
df= df['Categories'].tolist()

class dental_city_scraper(scrapy.Spider):
    
    custom_settings = {
        'DOWNLOAD_DELAY' : 0.25,
        'RETRY_TIMES': 10,
        "DOWNLOAD_TIMEOUT": 360,
        # export as CSV format
        'FEED_FORMAT' : 'csv',
        # 'FEED_URI' : 'New-Dental-city-data-with-category.csv',
    #     "ROTATING_PROXY_LIST" : ["108.59.14.208:13040", "108.59.14.203:13040"],
    #     "DOWNLOADER_MIDDLEWARES" : {
    #             "rotating_proxies.middlewares.RotatingProxyMiddleware" : 610,
    #             "rotating_proxies.middlewares.BanDetectionMiddleware" : 620}
    }
     
    name= 'scraper'
    
    def start_requests(self):
        for url in df:

            yield scrapy.Request(url=url, callback=self.parse)
    def parse(self,response):
        baseurl = 'https://www.staples.com'
        links = response.css("a.seo-component__seoLink::attr(href)").extract() 
        if len(links)<1:
            links =response.css("a.link-box__link_wrapper::attr(href)").extract()
        
        for link in links:
            print("link",link)
            yield scrapy.Request(url=baseurl+link, callback=self.parse_p_links)
            
    
    def parse_p_links(self, response):
        print("Response", response.url)
        
        
        
        
        
        
process = CrawlerProcess()
process.crawl(dental_city_scraper)
process.start()   