__author__ = 'zhengyiwang'
import scrapy
from appsCrawl.items import AppscrawlItem

class AppSpider(scrapy.Spider):
    name = "appS"
    allowed_domains = ["appstore.huawei.com"]
    start_urls = ["http://appstore.huawei.com/more/all"]
    total = 41
    for i in range(2, total + 1):
        start_urls.append(start_urls[0] +"/"+ str(i))
    print "allurl"
    print start_urls


    def parse(self, response):
        filename = response.url.split("/")[-1] + '.html'
        #with open(filename, 'wb') as f:
         #   f.write(response.body)

        for href in response.css("div.unit-main > div > div.game-info.whole > h4 >  a::attr('href')"):
            url = response.urljoin(href.extract())
            print "--------------------print for " + filename
            print url
            yield scrapy.Request(url, callback=self.parse_dir_content)



    def parse_dir_content(self, response):
        item = AppscrawlItem()
        detail = response.xpath('//div[@class="app-function nofloat"]')
        item['title'] = detail.xpath('a/@name').extract()[0]
        item['appId'] = detail.xpath('a/@appid').extract()[0]
        item['icon'] = detail.xpath('a/@icon').extract()[0]
        item['desc'] = response.xpath('//div[@id="app_strdesc"]/text()').extract()
        #print "................this is one item......."
        #print item['desc'], item['title'], item['appId'], item['icon']
        #print item
        return item




