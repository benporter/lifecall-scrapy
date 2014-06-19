from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector, HtmlXPathSelector
from ..items import LifecallItem
import re

class LifecallSpider(CrawlSpider):

    name = 'lifecall'
    allowed_domains = ['lifecall.org']
    start_urls = ['http://www.lifecall.org/cpc.html']
    rules = [Rule(SgmlLinkExtractor(allow=('/cpc/\w+\.html')), callback='parse_lifecall',follow=True)]

    def parse_lifecall(self, response):
        sel = Selector(response)
        page = LifecallItem()
        page['url'] = response.url 
        page['state'] = sel.select('//h3[@class="state-name"]/text()').extract()
        page['fulltext'] = sel.select('//div[@id="inside-content"]/div//p/text()').extract()
        page['links'] = sel.select('//div[@id="inside-content"]/div//a/text()').extract()
        return page
     

