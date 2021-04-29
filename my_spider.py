import scrapy

class CrawlQuotesSpider(scrapy.Spider):
  
    name = "crawl_opinions"
    
    def start_requests(self):
        #predefinded pages to crawl
        urls = ['https://www.debate.org/opinions/?sort=popular']
        for url in urls:
            request = scrapy.Request(url=url, callback=self.parse_main_url)
            #request.meta['tag_name'] = url.split('/')[-1]
            yield request

    def parse_main_url(self, response):
        pop_urls_list = response.css('.a-image-contain')
        for i in range(0,5):
            url = pop_urls_list[i].xpath('@href').extract()[0]
            final_url = "https://"+response.request.url.split('/')[2]+url
            request = scrapy.Request(url=final_url, callback=self.parse_secondary_urls)
            yield request

    def parse_secondary_urls(self, response):
        print(response)
