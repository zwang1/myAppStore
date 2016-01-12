__author__ = 'zhengyiwang'
import scrapy
from appsCrawl.items import AppscrawlItem
from scrapy.selector import Selector

class AppSpider(scrapy.Spider):
    name = "appProxy"
    allowed_domains = ["appstore.huawei.com"]
    start_urls = ["http://appstore.huawei.com/more/all"]

    '''
    def start_requests(self):
        #use splash server to parse the js first in order to get the next page href in html
        for url in self.start_urls:
            yield scrapy.Request(url, self.parse, meta={
                'splash':{
                    'endpoint':'render.html',
                    'args':{'wait':0.5}
                }
            })
    '''
    def parse(self, response):
        filename = response.url.split("/")[-1] + '.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        page = Selector(response)


        appsurl = page.xpath('//h4[@class="title"]/a/@href')

        for app in appsurl:
            url = app.extract()
            print "--------------------print apps for " + filename
            print url
            yield scrapy.Request(url, callback=self.parse_dir_content)

        # get the next page url
        page_ctrl = page.xpath('//div[@class="page-ctrl ctrl-app"]/a/@href')

        if len(page_ctrl) > 4:
            nextpage = page_ctrl[-2].extract()

            print "--------------------print for " + filename
            print "next page is " + nextpage

            yield scrapy.Request(nextpage, self.parse)


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
