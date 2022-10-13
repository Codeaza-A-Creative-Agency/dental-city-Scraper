import scrapy 
from scrapy.crawler import CrawlerProcess
import pandas as pd
#...
df= pd.read_csv('Dental-City-Product-urls.csv')
links= df['Links'].tolist()

class p_links_scraper(scrapy.Spider):
    name= 'p_links_scraper'
    
    def start_requests(self):
        for url in links:

            yield scrapy.Request(url=url, callback=self.parse)
    def parse(self,response):
        manufacture=response.css('span.desktopproductname ::text').extract_first()
        baseurl='https://dentalcity.com'
        att_url =response.xpath("//div[@class='dc-product-sheet']/a/@href").extract()
        # att_url = ''.join(baseurl+url)
        manufacture = manufacture.split('-')[0]
        descrip =response.css('div.dc-product-detail ::text').extract()
        descrip= ''.join(str(stri) for stri in descrip)
        yield{
            "Seller Platform": "Dental City",
            "Seller SKU":response.xpath("//meta[@itemprop='sku']/@content").extract_first(),
            "Manfacture":manufacture,
            "Manufacture Code":response.xpath("//meta[@itemprop='mpn']/@content").extract_first(),
            "Product Title":response.css('span.desktopproductname ::text').extract_first(),
            "Description":descrip,
            "Packaging":descrip,
            "Qty":descrip,
            "Categories": response.xpath("(//ul[@class='clearfix']/li/a/span/text())[2]").extract_first(),
            "Product Page URL":response.url,
            "Attachment URL":att_url,
                # response.xpath("//a[@class='dc-product-detail-link']/@href").extract()
            'Image URL':response.xpath("//img[@itemprop='image']/@src").extract()
            
            
        }

        # (//select[@id='skulist']/option/text())[2]
process = CrawlerProcess()
process.crawl(p_links_scraper)
process.start()