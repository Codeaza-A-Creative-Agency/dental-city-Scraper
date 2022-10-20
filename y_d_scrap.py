import scrapy
import re
import json
from scrapy.crawler import CrawlerProcess 
class yd_scrap(scrapy.Spider):
    name='scrap'
    custom_settings = {
        'DOWNLOAD_DELAY' : 0.25,
        'RETRY_TIMES': 10,
        # export as CSV format
        'FEED_FORMAT' : 'csv',
        'FEED_URI' : 'young-dental-data.csv'
    }
    start_urls=['https://youngdental.com/products/all-products/']
    
    def parse(self,response):
        
        links= response.xpath("//div[@class='product-box']/a/@href").extract()
        
        
        next_page= response.xpath("//a[@class='next page-numbers']/@href").extract_first()
        
        if next_page is not None:
            yield response.follow(url=next_page, callback=self.parse)
        
        
        for url in links:
            yield scrapy.Request(url=url, callback=self.parse_products)
        
    def parse_products(self,response):
        sc = response.xpath('(//script[@type="application/ld+json"]/text())[2]').extract_first()
        data= json.loads(sc)
        try:
            cat =data['@graph'][0]['itemListElement'][1]['item']['name']
        except:
            cat= response.xpath("(//nav[@class='woocommerce-breadcrumb']/a/text())[3]").extract_first()
        try:
            subcat= data['@graph'][0]['itemListElement'][2]['item']['name']
        except:
            subcat=response.xpath("(//nav[@class='woocommerce-breadcrumb']/a/text())[4]").extract_first()
        try:
            name =response.xpath("//h1[@class='product_title entry-title']/text()").extract_first()
        except:
            name =data['@graph'][0]['itemListElement'][3]['item']['name']
        descrip1= response.xpath("//div[@class='woocommerce-product-details__short-description']//p//text()").extract()
        descrip1 = ''.join(str(stri) for stri in descrip1)
        descrip2= response.xpath("//div[@class='panel faq-accoordian']//text()").extract()
        descrip2 = ''.join(str(stri) for stri in descrip2)
        descrip = descrip1 + descrip2
        try:
            sku =data['@graph'][1]['sku']
        except:
            sku = response.xpath("//span[@class='variable_skus']/span/text()").extract_first().replace('Item #','')
        pkgqty = response.xpath("(//select[@id='pa_product-quantity']/option)[2]/text()").extract_first()
        result = re.split(r'(-?\d*\.?\d+)', pkgqty)
        qty = result[1]
        pkg= result[2]
        yield{
            "Seller Platform": "Young Dental",
            "Seller SKU": sku,
            "Manufacture":'Young Dental',
            "Manufacture Code":sku,
            "Product Title": name,
            "Description":descrip,
            "Packaging":pkg,
            "Qty":qty,
            "Categories":cat,
            "Subcategories":subcat,
            "Product Page URL": response.url,  
            "Attachement":response.xpath("//div[@class='panel']/p/a/@href").extract_first(),
            "Image URL":response.xpath("//div[@class='woocommerce-product-gallery__image']/a/img/@src").extract()
        }






process = CrawlerProcess()
process.crawl(yd_scrap)
process.start()