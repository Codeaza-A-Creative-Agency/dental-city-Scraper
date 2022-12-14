from scrapy.http import FormRequest
import scrapy 
from scrapy.crawler import CrawlerProcess
import re

class dental_city_scraper(scrapy.Spider):
    
    custom_settings = {
        'DOWNLOAD_DELAY' : 0.25,
        'RETRY_TIMES': 10,
        # export as CSV format
        'FEED_FORMAT' : 'csv',
        'FEED_URI' : 'dental-city-data.csv'
        # "ROTATING_PROXY_LIST" : ["108.59.14.208:13040", "108.59.14.203:13040"],
        #         "DOWNLOADER_MIDDLEWARES" : {
        #         "rotating_proxies.middlewares.RotatingProxyMiddleware" : 610,
        #         "rotating_proxies.middlewares.BanDetectionMiddleware" : 620}
    }
     
    name= 'scraper'
    start_urls =['https://www.dentalcity.com/category/2/shop-category']
    def parse(self,response):
        links =response.css("li.categoriesdesc>a::attr(href)").getall()

        
        for link in links:
            # print(link.split("/")[4])
            data = {
            'param1': str(link.split("/")[4]),
            'param2': 'html_subcategorylist',
            'param3': '150X177',
            'param6': '',
            'param7': '?custid=&amp;custclsid=2',
        }
            # data = json.dumps(data)
            url = "https://www.dentalcity.com/widgets-category/gethtml_subcategoryproductlist"
            yield FormRequest(url,formdata=data, callback=self.parse_product_page)
            # yield scrapy.Request(url=url, method='POST',body=data,headers=headers,callback=self.parse_product_page)
    def parse_product_page(self,response):
        # print("Response",response.text)
        links = response.css(".category-name a::attr(href)").getall()
        for link in links:
            yield scrapy.Request(url=link, callback=self.parse_allproduct_page)
    def parse_allproduct_page(self,response):
        data = {
            'source': 'NarrowSrchData',
            'filter': response.url.split('/')[4],
            'hdnCategoryId': response.url.split('/')[4],
            'hdnCurrentProductIds': '',
            'hdnFilter': response.url.split('/')[4],
            'hdnSortType': 'SELLERRECOMMENDATION',
            'hdnProdPerPage': '31000'
}
        url = 'https://www.dentalcity.com/widgets-category/gethtml_productlist/1292/html_productlist/300X210'
        yield FormRequest(url,formdata=data, callback=self.parse_p_links)
    def parse_p_links(self,response):
        links = response.css("li.prodimage>a::attr(href)").extract()
        
        
        for link in links:
            yield scrapy.Request(url=link, callback=self.parse_product)     
       
    def parse_product(self,response):
        Seller="Dental City"
        
        names= response.xpath('//div[@class="schema"]/meta[@itemprop="name"]/@content').extract()
        skus = response.xpath('//meta[@itemprop="sku"]/@content').extract()
        description =response.xpath('//meta[@itemprop="description"]/@content').extract()
        description=''.join(description)
        description = re.sub(r"\s+"," ",description)
        mpn =response.xpath('//meta[@itemprop="mpn"]/@content').extract()
        category=response.xpath('//meta[@itemprop="category"]/@content').extract()
        prod= zip(names,skus,mpn,category)
        att_url = response.xpath("//div[@class='dc-product-sheet']/a/@href").extract()
        att_url = ["https://www.dentalcity.com"+url for url in att_url]
        mfg_name= response.xpath('//meta[@property="og:title"]/@content').extract_first().split('-')[0]
        for name,sku,mpn,category in prod:
            cat = category.split('/')[0]
            sub_cat= category.split('/')[1]
            try:
                qty = re.search('(.+)/(\D*)',description).group(1)
                pkg= re.search('(.+)/(\D*)',description).group(2)
            except:
                qty = ''
                pkg= ''
            skuid=response.url.split('/')[4]

            url = f'https://www.dentalcity.com/Widgets-product/gethtml_skulist/{skuid}/html_options3/false///'
            
            
            yield scrapy.Request(url=url, callback=self.parse_skuIDs, meta={"sku":skuid, "URL":response.url,
            "S-P":Seller,"Mfg-name":mfg_name,
            "Aurl":att_url,
            "Pkg":pkg,"qty":qty,
            "Description":description, "Cat":cat, "Sub-cat":sub_cat
            })
      
    def parse_skuIDs(self,response):
       
        
        variant_id = response.xpath('//select[@id="skulist"]/option/@value').extract()
        for v_id in variant_id:
            url=f'https://www.dentalcity.com/widgets-product/gethtml_filtered_apparelsku/{response.meta.get("sku")}/SkuId%24%24{v_id}%24%24true%24%24v/900X380/html_consumer-electronics1sku/param5/param6'
            yield scrapy.Request(url=url, callback=self.parse_data, meta={"Variant ID":v_id, "SKU":response.meta.get("sku"),
            "Mfg-name":response.meta.get("Mfg-name"),
            "AURL":response.meta.get("Aurl"),
            "Pkg":response.meta.get("Pkg"), "Qty":response.meta.get("Qty"),
            "Description":response.meta.get("Description"),"Cat":response.meta.get("Cat"),"sub":response.meta.get("Sub-cat")
            ,"URL":response.meta.get("URL"), "S-P":response.meta.get('S-P')})
  
            
            
            
    def parse_data(self,response):
        
        try:
            images=response.xpath('//a[@data-zoom-id="Zoom-1"]/img/@src').extract()
            images.append(response.xpath('//a[@id="Zoom-1"]/img/@src').extract_first())
        except:
            images=response.xpath('//a[@id="Zoom-1"]/img/@src').extract()
            
        yield{
            "Seller Platform":response.meta.get('S-P'),
            "Seller SKU": response.xpath('//div[@class="skuname"]//span[@id="skucode"]/text()').extract_first(),
            "Manufacture Name":response.meta.get("Mfg-name"),
            "Manufacture Code":response.xpath('//div[@class="mfgparts"]/span/text()').extract_first(),
            "Product Title":response.xpath("//div[@class='skuname']/span[@id='skuname']/text()").extract_first(),
            "Description":response.meta.get("Description"),
            "Packaging":response.meta.get("Pkg"),
            "Qty":response.meta.get("Qty"),
            "Categories":response.meta.get("Cat"),
            "Subcategories":response.meta.get('sub'),
            "Product URL":response.meta.get("URL"),
            "Attachment":response.meta.get("AURL"),
            "Image URL": images,            
        }

        
      
 
    
    


process = CrawlerProcess()
process.crawl(dental_city_scraper)
process.start()