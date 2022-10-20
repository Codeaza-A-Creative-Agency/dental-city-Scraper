
import scrapy 
import re
from scrapy.crawler import CrawlerProcess 
class yp_scrap(scrapy.Spider):
    name='scrap'
    custom_settings = {
        'DOWNLOAD_DELAY' : 0.25,
        'RETRY_TIMES': 10,
        # export as CSV format
        'FEED_FORMAT' : 'csv',
        'FEED_URI' : 'New-Young-Specialists-data-1.csv'
    }
    start_urls=['https://www.youngspecialties.com/product-category/orthodontics/',
                'https://www.youngspecialties.com/product-category/uncategorized/',
                'https://www.youngspecialties.com/product-category/plak-smacker/',
                'https://www.youngspecialties.com/product-category/endodontics/'
                ]

    def parse(self,response):
        links= response.xpath('//a[@class="overlay-card-link"]/@href').extract()
        
        next_page = response.xpath('//a[@class="next page-numbers"]/@href').extract_first()
        
        if next_page is not None:
            yield response.follow(url=next_page , callback=self.parse)
        
        
        for link in links:
           yield scrapy.Request(url=link, callback=self.parse_products)
    def parse_products(self, response):
        try:
            title= response.css('h1.product_title ::text').extract_first()
        except:
            title= response.css('h2.prod-title ::text').extract_first()
        pkgqty=re.search('(\d+)+\s*(ct)',title)
        
        try:
            qty =pkgqty.group(1)
            pkg= pkgqty.group(2)
        except:
            qty =''
            pkg=''
        try:
            size = response.xpath("(//select[@class='']/option/text())[2]").extract_first()
        except:
            pass
            size=''
        descript1= response.xpath("//div[@id='tab-description']/p//text()").extract()
        descript1= ''.join(str(stri) for stri in descript1)
        descrip2= response.xpath("//div[@id='tab-description']//ul//li/text()").extract()
        descrip2 = ''.join(str(stri) for stri in descrip2)
        descrip = descript1+descrip2
  
        
        try:
            title= title +"-"+ size
        except:
            pass
        yield{
            "Seller Platform": "Young Specialists",
            "Seller SKU":response.css('h5.yi-item-code ::text').extract_first().replace('Item #', ''),
            "Manufacture": "Young Specialists",
            "Manufacture Code":response.css('h5.yi-item-code ::text').extract_first().replace('Item #', ''),
            "Product Title":title,
            # response.css('h1.product_title ::text').extract_first(),
            "Description":descrip,
            "Packaging":pkg,
            "Qty":qty,
            "Categories":response.xpath("(//nav[@class='woocommerce-breadcrumb']/a/text())[2]").extract_first(),
            "Subcategories":response.xpath("(//nav[@class='woocommerce-breadcrumb']/a/text())[3]").extract_first(),
            "Product Page URL":response.url,
            "Image URL":response.xpath('//img[@class="attachment-thumbnail size-thumbnail"]/@src').extract()
        }
      

process = CrawlerProcess()
process.crawl(yp_scrap)
process.start()