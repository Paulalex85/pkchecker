#Tessier Paul-Alexandre
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.crawler import CrawlerProcess
import csv
import urllib
import sys


URL_base = sys.argv[1]
if URL_base.endswith('/'):
    URL_base = URL_base[:-1]
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
wrong_type = ["png","jpg","jpeg","gif","doc","zip","pdf","txt"]

nom_fichier = DOMAIN.split(".")
c = csv.writer(open("Rapport_Pkchecker_"+ nom_fichier[0] +".csv", "wb"))
c.writerow(["Url","Piwik","Version"])

class MySpider(BaseSpider):
    name = "pkchecker"
    allowed_domains = [DOMAIN]
    start_urls = [
        URL_base
    ]
    
    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        
        check = False
        new_version = True
        for script in hxs.select('//script/text()').extract():
            if 'Piwik.getTracker' in script:
                new_version = False
            if 'piwik.php' in script:
                check = True
        
        if check == True:
            if new_version == True:
                c.writerow([response.url,"Present", "Nouvelle Version"])
            else:
                c.writerow([response.url,"Present","Ancienne Version"])
        else:
            c.writerow([response.url,"Non","-"])
        
        for url in hxs.select('//a/@href').extract():
            if not ( url.startswith('http://') or url.startswith('https://') ):
                if not url.startswith('/'):
                    url = URL_base + '/' + url
                else:
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
