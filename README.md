lifecall-scrapy
===============

Using the python scrapy module to pull info off of lifecall.org.  

Problem statement:  mom was about to hand write hundreds of addresses from this website, so I offered to build a webscrawler instead.



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

