__author__ = 'zhengyiwang'
import random
import logging

from scrapy.conf import settings
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware

class RandomUserAgentMiddleware(UserAgentMiddleware):
    def __init__(self, settings, user_agent = 'Scrapy'):
        print "agent init"
        super(RandomUserAgentMiddleware, self).__init__()
        self.user_agent = user_agent

    def process_request(self, request, spider):
        print "agent parse request"
        ua  = random.choice(settings.get('USER_AGENT_LIST'))
        print "*******current agent is %s ***" %ua
        if ua:
            request.headers.setdefault('User-Agent', ua)