import scrapy
import json

class CrawlPopularOpinionsSpider(scrapy.Spider):
    name = "debate_crawler"

    def start_requests(self):
        """Call the debates.org website"""
        #predefinded pages to crawl
        urls = ['https://www.debate.org/opinions/?sort=popular']
        for url in urls:
            request = scrapy.Request(url=url, callback=self.parse_main_url)
            yield request

    def parse_main_url(self, response):
        """Returns the object of URLs or top 5 popular opinions"""
        pop_urls_list = response.css('.a-image-contain')
        for i in range(5):#top 5 popular opinions
            url = pop_urls_list[i].xpath('@href').extract()[0]
            final_url = "https://"+response.request.url.split('/')[2]+url
            request = scrapy.Request(url=final_url, callback=self.parse_secondary_urls)
            yield request

    def parse_secondary_urls(self, response):
        """Returns the json dictionary from the argument page"""
        # post_url = 'https://www.debate.org/opinions/~services/opinions.asmx/GetDebateArgumentPage'
        topic = response.css('h1 ::text').getall()[0]
        category = response.css('#breadcrumb a')[2].css('::text').getall()[0]
        yes_args = response.css('#yes-arguments li').css('.hasData')
        no_args = response.css('#no-arguments li').css('.hasData')
        l_yes = self.parse_title_body(yes_args)
        l_no = self.parse_title_body(no_args)
        json_dict = {"topic": topic, "category": category, "pro_arguments":l_yes,"con_arguments":l_no}
        yield json_dict
        #pros_args = args.css("#yes-arguments")
        #opinions = pros_args.css('.hasData')
        #for opi in opinions:
        #    title = opi.xpath('h2')
        #    str_opinion = opi.xpath('p')
        #    print(title)
        #id = opinions[0].xpath('@did').extract()[0]
        #str_json = {'debateId': str(id), 'pageNumber': 2,'itemsPerPage':10,'ysort':5,'nsort':5}
        #post_body = json.dumps(str_json)
        #yield scrapy.Request(url=post_url,method='POST',headers={'Content-Type':'application/json'},body=post_body, callback=self.parse_post_request)

    def parse_title_body(self,args):
        """Return the list of title and body of pro and con according to the parameters

        Parameters
        ----------
        args
            The type of arguments eg. "yes-arguments", "no-arguments"
        
        Returns
        -------
        l:list
            A list of all the "h2" as key of "title" and text of "p" as "body"
        """
        l = []
        for ar in args:
            h2_tags = ar.css('h2 ::text').getall()
            p_tags = ar.css('p ::text').getall()
            comment = ""
            for txt in p_tags:
                comment += txt
            l.append({"title":h2_tags[0],"body":comment})
        return l
    
    # To be explored
    def parse_post_request(self, response):
        print("********************************")
        json_response = json.loads(response.text)
        response_str = json_response["d"]
        selector_body = scrapy.Selector(text=response_str)
        #title = selector_body.xpath("")
        print("********************************")
        pass
    