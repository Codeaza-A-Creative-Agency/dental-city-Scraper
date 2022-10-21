import scrapy 
from scrapy.crawler import CrawlerProcess
import pandas as pd
import re
df=pd.read_csv('Dental-City-Product-urls.csv')
links= df['Links'].tolist()

class dental_city_scraper(scrapy.Spider):
    
    custom_settings = {
        'DOWNLOAD_DELAY' : 0.25,
        'RETRY_TIMES': 10,
        # export as CSV format
        'FEED_FORMAT' : 'csv',
        'FEED_URI' : 'New-Dental-city-data-with-category.csv'
    }
     
    name= 'scraper'
    
    def start_requests(self):
        for url in links:

            yield scrapy.Request(url=url, callback=self.parse)
    def parse(self,response):
        manufacture=response.css('span.desktopproductname ::text').extract_first()
        baseurl='https://dentalcity.com'
        att_url =response.xpath("//div[@class='dc-product-sheet']/a/@href").extract()
        att_url = ','.join(baseurl+url for url in att_url)
        manufacture = manufacture.split('-')[0]
        descrip =response.css('div.dc-product-detail ::text').extract()
        category= response.xpath("(//meta[@itemprop='category']/@content)[1]").extract_first()
        try:
            pkgqty= response.xpath("(//meta[@itemprop='name']/@content)[1]").extract_first()
            pkg =pkgqty.split('/')[1]
            qty = pkgqty.split('/')[0]
            for word in qty:
                if word.isdigit():
                    qty=word
        except:
            pass
            try:
                descrip= ''.join(str(stri) for stri in descrip)
            except:
                descrip='Null'
            try:
                qty = re.search('(.+)/(\D*)',descrip).group(1)
                pkg= re.search('(.+)/(\D*)',descrip).group(2)
            except:
                qty='Null'
                pkg='Null'
        yield{
            "Seller Platform": "Dental City",
            "Seller SKU":response.xpath("//meta[@itemprop='sku']/@content").extract_first(),
            "Manfacture":manufacture,
            "Manufacture Code":response.xpath("//meta[@itemprop='mpn']/@content").extract_first(),
            "Product Title":response.css('span.desktopproductname ::text').extract_first(),
            "Description":descrip,
            "Packaging":pkg,
            "Qty":qty,
            "Categories":category,
            "Product Page URL":response.url,
            "Attachment URL":att_url,
            'Image URL':response.xpath("//img[@itemprop='image']/@src").extract()
            
            
        }

process = CrawlerProcess()
process.crawl(dental_city_scraper)
process.start()