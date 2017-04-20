from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.crawler import CrawlerProcess
import csv
import urllib
import sys

#URL_base = sys.argv[1]
URL_base = "https://www.ronan-chardonneau.fr"
DOMAIN = URL_base

if URL_base.startswith('http://'):
    DOMAIN = DOMAIN[7:]
elif URL_base.startswith('https://'):
    DOMAIN = DOMAIN[8:]

print(DOMAIN)
global list_urls
global c
global wrong_type
list_urls = [URL_base]
wrong_type = ["png", "jpg","jpeg","gif","doc","zip","pdf","txt"]

class MySpider(BaseSpider):
    name = "test"
    allowed_domains = [DOMAIN]
    start_urls = [
        URL_base
    ]
    
    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        
        check = False
        for script in hxs.select('//script/text()').extract():
            if 'piwik.php' in script:
                check=True
                break
        
        if check == True:
            print "<tr><td>"+ response.url +"</td><td>Present</td></tr>"
        else:
            print "<tr><td>"+ response.url +"</td><td>Non</td></tr>"
        
        for url in hxs.select('//a/@href').extract():
            if not ( url.startswith('http://') or url.startswith('https://') ):
                url = URL_base + url
            if not url in list_urls:
            	if DOMAIN in url:
            	    s = url.split(".")
            	    if any(word in s[-1] for word in wrong_type):
            	        x = 1
                    else:
                        list_urls.append(url)
                        yield Request(url, callback=self.parse)
                    

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(MySpider)
process.start()
