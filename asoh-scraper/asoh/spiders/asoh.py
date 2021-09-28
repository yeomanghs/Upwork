import scrapy
from asoh.items import AsohItem
from scrapy.http import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import bs4
from datetime import datetime
import re

class AsohSpider(CrawlSpider):
    name = 'asoh'
    allowed_domains = ['myfcd.moh.gov.my']
    start_urls = ['http://myfcd.moh.gov.my/index.php/1997-food-compositon-database']
    rules = (Rule(LinkExtractor(restrict_xpaths=["//a[contains(@title,'Next')]"]), callback='parse_item', follow=True),)
	
    def parse_start_url(self,response):
        yield self.parse_item(response)
		
    def parse_item(self,response):
        for i in response.xpath("//tbody/tr[@class = 'cat-list-row0']"):	
            asoh_info = AsohItem()
            asoh_info['Category'] = i.xpath("td[3]/text()").extract()[0]
            asoh_info['ProductName'] = i.xpath("td[2]/a/text()").extract()		
            page = i.xpath("td/a/@href").extract()[0]
            request = scrapy.Request("http://myfcd.moh.gov.my" + page,callback = self.parseDetails)
            request.meta['asoh_info'] = asoh_info
            yield request
            			
    def parseDetails(self,response):
        asoh_info = response.meta['asoh_info']
        nutrients = [i for i in response.xpath("//table[@width='70%']/tr/td/text()").extract() if '\xa0' not in i]		
        asoh_info['Nutrients_Comp'] = ['-'.join(z) for z in zip([i for i in nutrients[0::3]],
        [''.join(x) for x in zip(nutrients[1::3],nutrients[2::3])])]
        yield asoh_info

        