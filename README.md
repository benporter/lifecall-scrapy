lifecall-scrapy
===============

Using the python scrapy module to pull info off of <a href="http://www.lifecall.org/cpc.html">lifecall.org</a>.  

Problem statement:  mom was about to hand write hundreds of addresses from this website, so I offered to build a webscrawler instead.

What I found helpful:
 - Dan Koch's <a href="https://github.com/pythonclt/scrapy-intro/blob/master/presentation.md">scrapy intro presentation</a> at the Charlotte Python Meetup
 - Scrapy <a href="http://doc.scrapy.org/en/latest/intro/tutorial.html">tutorial<a/>
 - newcoder.io web scraping <a href="http://newcoder.io/scrape/">tutorial<a/>

===============

Install the scrapy module

    #!/bin/bash
    sudo pip install scrapy
    
Create the project, which builds out most of the necessary files.

    #!/bin/bash
    scrapy startproject lifecall
    
Edit lifecall/lifecall/items.py to add the fields you want to scrape.  In my case, it was three things: the source url, the state name and the fulltext, which is all of the addresses and phone numbers.

    from scrapy.item import Item, Field
        
    class LifecallItem(Item):
        url = Field()
        state = Field()
        fulltext = Field()
            
In lifecall/lifecall/spiders/ add a .py file, name it whatevs.  I called mine lifecall_spider.py.  Here are the file contents:

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

A few noteworthy comments from lifecall_spider.py:
 - The allowed_domains option prevents the crawler from leaving this domain as it follows links
 - The rule is set to only scrape pages that have /cpc/<a word>.html, such as http://www.lifecall.org/cpc/north_carolina.html.  The w+ is why the regex module was imported, which captures any word.
 - The double forward slash, //, means get all instances of the path that follows it.  So //h3 means get all <h3></h3> tags from the page, not just one.

To run the spider, which pulls the the ~50 pages in approx 2-3 seconds, run the following from the command line:

    #!/bin/bash
    scrapy crawl lifecall -o scraped_data.json -t json

That outputs a .json file, and other options are available, such as csv and xml.

Finally, I ran another script, which was separate from the scrapy webcrawler project to read in the json data, and write it to a csv file.  That file, write_json_to_csv.py, is located in the lifecall/ directory.

    import json
    import re
    import csv

    f = csv.writer(open("addresses.csv", "wb+"))
    f.writerow(["state", "url", "address"])

    with open("scraped_data.json") as json_file:
        json_data = json.load(json_file)
      for j in json_data:
         try:
            temp_state = j['state'][0]
        except:
            temp_state = "Missing State"
        for t in j['fulltext']:
            f.writerow([temp_state,
                j['url'],
                re.sub('\s+',' ',t.encode('utf-8'))]) 

The result sits in lifecall/address.csv

QED

===============
**Scrapely**
===============
Initially I intended to use the <a href="https://github.com/scrapy/scrapely">scrapely</a> python module rather than scrapy, but needed to pull a dynamic number of addresses, which seemed easier with scrapy.  So here are the instructions for installing scrapely for a more model based approach to scraping.

===============

**Install and Setup**

Edit <b>/etc/apt/sources.list</b> to include the following line.  I am running Ubuntu 13, so put "saucy" but your machine could be different.

    deb http://archive.scrapy.org/ubuntu saucy main

Add the key

    curl -s http://archive.scrapy.org/ubuntu/archive.key | sudo apt-key add -

Update

    sudo apt-get update

If you got the following error after running the update, then look back at the curl step.  

    W: GPG error: http://archive.scrapy.org saucy InRelease: The following signatures couldn't be verified because the public key is not available: NO_PUBKEY 7AECB5E990E2741A

Install the scrapely module

    sudo apt-get install python-scrapely

