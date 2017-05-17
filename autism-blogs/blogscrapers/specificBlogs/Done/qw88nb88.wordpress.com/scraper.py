import scrapy

class test_spider(scrapy.Spider):
    name = "scraper"
    start_urls = ['https://qw88nb88.wordpress.com/']
    custom_settings = {
        'RETRY_TIMES': 10,
    }
    
    def parse (self, response):
      for href in response.xpath('//li[@id="archives-2"]/ul/li/a/@href'):
          if href.extract() !="":
            full_url = response.urljoin(href.extract())
            yield scrapy.Request(full_url, callback=self.parse_link)
    
    def parse_link(self, response):
      for postlink in response.xpath('//h2[@class="posttitle"]/a/@href'):
         full_url = response.urljoin(postlink.extract())
         yield scrapy.Request(full_url, callback=self.parse_post)

    def parse_post(self, response):
      try:
        stringdate = response.xpath('//p[@class="postdate"]/text()').extract()[0]
        stringdate = stringdate[:(len(stringdate) - 18)]
      except:
        stringdate = ""

      try:
        title = response.xpath('//h2[@class="posttitle"]/text()').extract()[0]
      except:
        title =""

      try:
        body = ""
        for content in response.xpath('//div[@class="postentry"]//*[not(descendant::div[@class="wpcnt"]) and not(ancestor-or-self::div[@class="wpcnt"]) and not(descendant::div[@id="jp-post-flair"]) and not(ancestor-or-self::div[@id="jp-post-flair"])]/text()'):
          body = body + content.extract() + ' '
      except:
        body =""
      
      try:
        outgoing_links = []
        for href in response.xpath('//div[@class="postentry"]//*[not(descendant::div[@class="wpcnt"]) and not(ancestor-or-self::div[@class="wpcnt"]) and not(descendant::div[@id="jp-post-flair"]) and not(ancestor-or-self::div[@id="jp-post-flair"])]/@href'):
          extracted = href.extract()
          if 'https://qw88nb88.wordpress.com' not in extracted:
            outgoing_links.append(extracted)
      except:
        outgoing_links = []
      


      yield {
          'date' : stringdate,
          'body' : body,
          'link': response.url,
          'title': title,
          'outgoing_links': outgoing_links
        }