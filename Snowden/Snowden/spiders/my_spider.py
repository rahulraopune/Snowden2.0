import scrapy
import json
import requests
import time
from scrapy.crawler import CrawlerProcess


class CrawlPopularOpinionsSpider(scrapy.Spider):
    name = "debate_crawler"

    def start_requests(self):
        """Call the debates.org website"""
        # predefinded pages to crawl
        urls = ['https://www.debate.org/opinions/?sort=popular']
        for url in urls:
            request = scrapy.Request(url=url, callback=self.parse_main_url)
            yield request

    def parse_main_url(self, response):
        """Returns the object of URLs or top 5 popular opinions"""
        pop_urls_list = response.css('.a-image-contain')
        for i in range(5):  # top 5 popular opinions
            url = pop_urls_list[i].xpath('@href').extract()[0]
            final_url = response.request.url.split('/opinions')[0]+url
            request = scrapy.Request(
                url=final_url, callback=self.parse_secondary_urls)
            yield request

    def parse_secondary_urls(self, response):
        """Returns the json dictionary from the argument page"""
        topic = response.css('h1 ::text').getall()[0]
        category = response.css('#breadcrumb a')[2].css('::text').getall()[0]
        yes_args = response.css('#yes-arguments li').css('.hasData')
        no_args = response.css('#no-arguments li').css('.hasData')
        l_yes = self.parse_title_body(yes_args)
        l_no = self.parse_title_body(no_args)
        button = response.css('.debate-more-holder')
        if len(button) == 0:
            json_dict = {"topic": topic, "category": category,
                         "pro_arguments": l_yes, "con_arguments": l_no}
            yield json_dict
        else:
            page = 2
            while page >= 2:
                print("--------------------------")
                post_url = 'https://www.debate.org/opinions/~services/opinions.asmx/GetDebateArgumentPage'
                headers = {'content-type': "application/json", 'cache-control': "no-cache",
                           'postman-token': "4e6a9794-a2e7-479a-0d7f-2aa9a7a87367"}
                id = response.css(
                    '#yes-arguments li')[0].xpath('@did').extract()[0]
                str_json = {'debateId': str(
                    id), 'pageNumber': page, 'itemsPerPage': 10, 'ysort': 5, 'nsort': 5}
                post_body = json.dumps(str_json)
                res = requests.request(
                    method='POST', url=post_url, headers=headers, data=post_body)
                html_str = json.loads(res.text)['d']
                if html_str != '{ddo.split}{ddo.split}finished':
                    pos_neg_atr_list = html_str.split('{ddo.split}')
                    pos_html = pos_neg_atr_list[0]
                    neg_html = pos_neg_atr_list[1]
                    pos_selector = scrapy.Selector(text=pos_html)
                    neg_selector = scrapy.Selector(text=neg_html)
                    pos_args = pos_selector.css('li').css('.hasData')
                    neg_args = neg_selector.css('li').css('.hasData')
                    list_pos_li_tags = self.parse_title_body(pos_args)
                    list_neg_li_tags = self.parse_title_body(neg_args)
                    l_yes.extend(list_pos_li_tags)
                    l_no.extend(list_neg_li_tags)
                    page += 1
                else:
                    break
            json_dict = {"topic": topic, "category": category,
                         "pro_arguments": l_yes, "con_arguments": l_no}
            yield json_dict

    def parse_title_body(self, args):
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
            l.append({"title": h2_tags[0], "body": comment})
        return l


#process = CrawlerProcess({'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'})
# rocess.crawl(CrawlPopularOpinionsSpider)
# process.start() # the script will block here until the crawling is finished
