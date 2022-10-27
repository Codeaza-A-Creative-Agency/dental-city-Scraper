import scrapy 
from scrapy.crawler import CrawlerProcess
import pandas as pd
import re
df=pd.read_csv('Dental-City-Product-URLs.csv')
links= df['Product URL'].tolist()
print(len(links))
links = links[:150]
class dental_city_scraper(scrapy.Spider):
    
    custom_settings = {
        'DOWNLOAD_DELAY' : 0.25,
        'RETRY_TIMES': 10,
        # export as CSV format
        'FEED_FORMAT' : 'csv',
        'FEED_URI' : 'testing2.csv'
    }
     
    name= 'scraper'
    
    def start_requests(self):
        for url in links:

            yield scrapy.Request(url=url, callback=self.parse)
    def parse(self,response):
        names= response.xpath('//div[@class="schema"]/meta[@itemprop="name"]/@content').extract()
        skus = response.xpath('//meta[@itemprop="sku"]/@content').extract()
        description =response.xpath('//meta[@itemprop="description"]/@content').extract()
        mpn =response.xpath('//meta[@itemprop="mpn"]/@content').extract()
        category=response.xpath('//meta[@itemprop="category"]/@content').extract()
        prod= zip(names,skus,mpn,category)
        att_url = response.xpath("//div[@class='dc-product-sheet']/a/@href").extract()
        mfg_name= response.xpath('//meta[@property="og:title"]/@content').extract_first().split('-')[0]
        for name,sku,mpn,category in prod:
            cat = category.split('/')[0]
            sub_cat= category.split('/')[1]
            descrip =''.join(str(string) for string in description)
            try:
                qty = re.search('(.+)/(\D*)',descrip).group(1)
                pkg= re.search('(.+)/(\D*)',descrip).group(2)
            except:
                qty = ''
                pkg= ''
            yield{
                "Seller Platform": "Dental City",
                "Seller SKU":sku,
                "Manufacture":mfg_name,
                "Manufacture Code":mpn,
                "Product Title":name,
                "Description":description,
                "Packaging":'pkg',
                "Qty":qty,
                'Categories':cat,
                "Subcategories":sub_cat,
                "Product Page URL":response.url,
                "Attachement URL":att_url,
                'Image URL':''
            }


process = CrawlerProcess()
process.crawl(dental_city_scraper)
process.start()