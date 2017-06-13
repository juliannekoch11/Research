import scrapy
from selenium import webdriver
import time

class test_spider(scrapy.Spider):
    name = "scraper"
    start_urls = ['http://autismnaturalvariation.blogspot.com/']
    custom_settings = {
        'RETRY_TIMES': 10,
    }

    def __init__(self):
        self.driver = webdriver.Firefox()
    
    def parse (self, response):
      self.driver.get(response.url)
      toclick = self.driver.find_elements_by_xpath('//span[@class="zippy"]')
      for x in toclick:
        webdriver.common.action_chains.ActionChains(self.driver).move_to_element(x).click(x).perform()
        time.sleep(1.5)
      for href in self.driver.find_elements_by_xpath('//ul[@class="posts"]/li/a'):
            full_url = response.urljoin(href.get_attribute("href"))
            yield scrapy.Request(full_url, callback=self.parse_link)
      self.driver.close()
    
    def parse_link(self, response):
      stringdate = response.xpath('//h2[@class="date-header"]/span/text()').extract()[0]
      title = response.xpath('//h3[@class="post-title entry-title"]/text()').extract()[0]
      body = ""
      for content in response.xpath('//div[@class="post-body entry-content"]/descendant-or-self::node()/text()'):
        body = body + content.extract() + ' '
      
      outgoing_links = []
      for href in response.xpath('//div[@class="post-body entry-content"]/descendant-or-self::a/@href'):
        extracted = href.extract()
        if 'http://autismnaturalvariation.blogspot.com' not in extracted:
          outgoing_links.append(extracted)
      yield{
      'link': response.url,
      'date': stringdate,
      'body': body,
      'title': title,
      'outgoing_links': outgoing_links
      }