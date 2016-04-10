# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector

from sjtu.items import SjtuItem


class SjtuSpiderSpider(CrawlSpider):
    name = 'sjtu_spider'
    allowed_domains = ['www.jwc.sjtu.edu.cn']
    start_urls = ['http://www.jwc.sjtu.edu.cn/web/sjtu/198072.htm']

    rules = (
        Rule(LinkExtractor(allow = (r'http://www\.jwc\.sjtu\.edu\.cn/web/sjtu/\d+', )), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        sel = Selector(response)
        item = SjtuItem()
        #zz_num = zz_num + 1
        #print zz_num
        #item['name'] = sel.xpath('//h1/span[@property="v:itemreviewed"]/text()').extract()
        print response.url
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        filename = 'url.txt'
        data = response.url + '\n'
        with open(filename, 'a') as f:
            f.write(data)
        return item
