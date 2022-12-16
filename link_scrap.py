import scrapy 
from scrapy.http import FormRequest
from scrapy import Request
from scrapy.crawler import CrawlerProcess
import json
class dental_city_scraper(scrapy.Spider):
    
  
    
    custom_settings = {
        'DOWNLOAD_DELAY' : 0.25,
        'RETRY_TIMES': 10,
        # export as CSV format
        'FEED_FORMAT' : 'csv',
        # 'FEED_URI' : 'New-Dental-city-data-with-category.csv',
    #     "ROTATING_PROXY_LIST" : ["108.59.14.208:13040", "108.59.14.203:13040"],
    #     "DOWNLOADER_MIDDLEWARES" : {
    #             "rotating_proxies.middlewares.RotatingProxyMiddleware" : 610,
    #             "rotating_proxies.middlewares.BanDetectionMiddleware" : 620}
    }
     
    name= 'scraper'
    start_urls =['https://www.dentalcity.com/category/2/shop-category']
    def parse(self,response):
        links =response.css("li.categoriesdesc>a::attr(href)").getall()
        headers = {
        'authority': 'www.dentalcity.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,ur;q=0.8,so;q=0.7,hi;q=0.6',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'cookie': '.ASPXANONYMOUS=5lZodko32QEkAAAANDQ2ZTM0MDYtNWFkNC00OTI0LTkxOTEtNmI5MDM5NGNiNWNjBdQ_Y2MCIlVPDFs3Cik62CpuEBs1; hoppersession=WebStore_SessionId=fpnwyw1bef5lyssxlcefflaa; hopperopened=0; WebStore_SessionId=4ia5t3ja0ygf44fdqzma1dwl; userdata=31f7ef98-aaeb-449f-8384-3da93fb88015; signuppopup=EmailSignUp_shown=1&WebStore_SessionId=4ia5t3ja0ygf44fdqzma1dwl',
        'dnt': '1',
        'origin': 'https://www.dentalcity.com',
        'referer': 'https://www.dentalcity.com',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }
        
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
            yield scrapy.Request(url=link, callback=self.parse_p_links)
    def parse_allproduct_page(self,response):
        headers = {
            'authority': 'www.dentalcity.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9,ur;q=0.8,so;q=0.7,hi;q=0.6',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            # 'cookie': '.ASPXANONYMOUS=5lZodko32QEkAAAANDQ2ZTM0MDYtNWFkNC00OTI0LTkxOTEtNmI5MDM5NGNiNWNjBdQ_Y2MCIlVPDFs3Cik62CpuEBs1; hoppersession=WebStore_SessionId=fpnwyw1bef5lyssxlcefflaa; hopperopened=0; WebStore_SessionId=ogzmc3jicot4wwrrvz354kh1; userdata=d55ca647-4b86-4ebb-8d8e-4586f9f7b72d; signuppopup=EmailSignUp_shown=1&WebStore_SessionId=ogzmc3jicot4wwrrvz354kh1',
            'dnt': '1',
            'origin': 'https://www.dentalcity.com',
            'referer': 'https://www.dentalcity.com/category/1292/bands-and-strips',
            'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }
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
        print(links)       
       
  

process = CrawlerProcess()
process.crawl(dental_city_scraper)
process.start()