__author__ = 'zhengyiwang'
import scrapy
from appsCrawl.items import AppListItem
from appsCrawl.items import AppscrawlItem

class AppSpider(scrapy.Spider):
    name = "appList"
    allowed_domains = ["appstore.huawei.com"]
    start_urls = ["http://appstore.huawei.com/topics"]
    total = 30
    for i in range(2, total + 1):
        start_urls.append(start_urls[0] +"/"+ str(i))



    def parse(self, response):
        filename = response.url.split("/")[-1] + '.html'
        #with open(filename, 'wb') as f:
         #   f.write(response.body)

        for href in response.xpath('//div[@class="topic-item-info content"]/h4/a/@href'):
            url = response.urljoin(href.extract())
            url = href.extract()
            print "--------------------print for " + filename
            print url
            yield scrapy.Request(url, callback=self.parse_list_content)

    def parse_list_content(self, response):
        item = AppListItem()
        item['title'] = response.xpath('//div[@class="topic-item-info content"]/h4/text()').extract()
        apps = response.xpath('//li[@class="info"]/h3/a/@href')


        item['list'] = apps.re('C[0-9]*')
        print"app list here"
        print item['title']
        print item['list']

        for link in apps:
            url = response.urljoin(link.extract())
            print url
            yield scrapy.Request(url, callback=self.parse_dir_content)




    def parse_dir_content(self, response):
        item = AppscrawlItem()
        detail = response.xpath('//div[@class="app-function nofloat"]')
        item['title'] = detail.xpath('a/@name').extract()[0]
        item['appId'] = detail.xpath('a/@appid').extract()[0]
        item['icon'] = detail.xpath('a/@icon').extract()[0]
        item['desc'] = response.xpath('//div[@id="app_strdesc"]/text()').extract()
        print "................this is one item......."
        print item['desc'], item['title'], item['appId'], item['icon']




