import scrapy
import json
import requests


class CrawlPopularOpinionsSpider(scrapy.Spider):
    """Implement crawler to crawl popular debate topics from debate.org"""
    name = "debate_crawler"

    def start_requests(self):
        """Call the debates.org website"""
        # predefined pages to crawl
        urls = ['https://www.debate.org/opinions/?sort=popular']
        for url in urls:
            request = scrapy.Request(url=url, callback=self.parse_main_url)
            yield request

    def parse_main_url(self, response):
        """Returns the object of URLs or top 5 popular opinions"""
        pop_urls_list = response.css('.a-image-contain')
        for i in range(5):  # top 5 popular opinions
            url = pop_urls_list[i].xpath('@href').extract()[0]
            final_url = "https://" + response.request.url.split('/')[2] + url
            request = scrapy.Request(url=final_url, callback=self.parse_secondary_urls)
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

        if len(button) != 0:
            page = 2
            while page >= 2:
                html_str = self.call_more_arguments(page, response)
                if html_str == '{ddo.split}{ddo.split}finished':
                    break
                self.extract_more_arguments(html_str, l_no, l_yes)
                page += 1
        json_dict = {"topic": topic, "category": category, "pro_arguments": l_yes, "con_arguments": l_no}
        yield json_dict

    def extract_more_arguments(self, html_str, l_no, l_yes):
        """Extract the arguments after they are loaded."""
        pos_neg_atr_list = html_str.split('{ddo.split}')
        self.separate_pros_cons(l_no, l_yes, pos_neg_atr_list)

    def separate_pros_cons(self, l_no, l_yes, pos_neg_atr_list):
        """Separate the positive and negative arguments in the extra loaded arguments.

        Parameters
        ----------
        l_no
            List of negative arguments.
        l_yes
            List of positive arguments.
        pos_neg_atr_list
            The split JSON list after the sending request to 'Load more arguments' button.
        """
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

    @staticmethod
    def call_more_arguments(page, response):
        """Call 'Load more arguments' button if it is available.

        Parameters
        ----------
        page
            The current page number.
        response
            The response after calling the url page

        Returns
        -------
        html_str
            The JSON response string after calling the post url of the button.
        """
        post_url = 'https://www.debate.org/opinions/~services/opinions.asmx/GetDebateArgumentPage'
        headers = {'content-type': "application/json"}
        debate_id = response.css('#yes-arguments li')[0].xpath('@did').extract()[0]
        str_json = {'debateId': str(debate_id), 'pageNumber': page, 'itemsPerPage': 10, 'ysort': 5, 'nsort': 5}
        post_body = json.dumps(str_json)
        res = requests.request(method='POST', url=post_url, headers=headers, data=post_body)
        html_str = json.loads(res.text)['d']
        return html_str

    @staticmethod
    def parse_title_body(args):
        """Return the list of title and body of pro and con according to the parameters

        Parameters
        ----------
        args
            The type of arguments eg. "yes-arguments", "no-arguments"

        Returns
        -------
        list_headers:list
            A list of all the "h2" as key of "title" and text of "p" as "body"
        """
        list_headers = []
        for arguments in args:
            h2_tags = arguments.css('h2 ::text').getall()
            p_tags = arguments.css('p ::text').getall()
            comment = ""
            for txt in p_tags:
                comment += txt
            list_headers.append({"title": h2_tags[0], "body": comment})
        return list_headers

# DEBUG in IDE
# process = CrawlerProcess({'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'})
# process.crawl(CrawlPopularOpinionsSpider)
# process.start() # the script will block here until the crawling is finished
