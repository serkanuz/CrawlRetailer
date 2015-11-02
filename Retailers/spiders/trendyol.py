import scrapy
from pyquery import PyQuery as pq
from scrapy.http import FormRequest
import json
from sets import Set
import time
import os
from tld import get_tld
from urlparse import urlparse

class TrendyolSpider(scrapy.Spider):
    name = "trendyol"
    processedLinks =Set([])
    tempLinks = set([])

    start_urls = ['http://www.trendyol.com/']


    def parse(self, response):
        self.processedLinks.add(response.url)
        d = pq(response.body)
        parsed_uri = urlparse( response.url )
        domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
        for l in d('a'):
            if not pq(l).attr('href') is None: 
                link = pq(l).attr('href').encode('utf-8')
                if not 'javascript' in link:
                    
                    if not link.startswith('http'):
                        link= domain+str(link)

                    path = '{uri.scheme}://{uri.netloc}/{uri.path}/'.format(uri=urlparse(link))

                    if not path in self.processedLinks and path.startswith(domain) and '/UrunDetay/' in path :
                        yield scrapy.Request(path, self.writeHtml)                 

                    if not path in self.processedLinks  and path.startswith(domain):    
                        yield scrapy.Request(path, self.parse)

    def writeHtml(self, response):
        self.processedLinks.add(response.url)
        today = time.strftime('%Y%m%d')
        parsed_uri = urlparse( response.url )
        domain = '{uri.netloc}'.format(uri=parsed_uri)
        directory = './html/'+today+'/'+domain
        if not os.path.exists(directory):
            os.makedirs('./html/'+today+'/'+domain)

        fileName = response.url.split("/")[-3]+"_"+response.url.split("/")[-2]+"_"+response.url.split("/")[-1]+".html"
        with open(directory+'/'+fileName, 'wb') as f:
            f.write(response.body)
