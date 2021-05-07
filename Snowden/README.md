# Computational Argumentation Assignment 1 
**Group : Snowden**

**Members :**

* Nihal Yadalam Murali Kumar
* Rahul Gururaja Rao
* Shivam Sharma
* Tejas Ravindra Dhawale

**File Structure** 
```bash
├── Snowden
│   ├── spiders
│   │   ├── _init_.py
│   │   ├── my_spider.py
│   ├── _init_.py
│   ├── items.py
│   ├── middlewares.py
│   ├── pipelines.py
│   ├── settings.py
├── BarGraph_category.png
├── BarGraph_topic.png
├── README.md
├── Histogram.png
├── plot.py
├── scrapy.cfg
```
**Required Libraries**

Make sure you have python and pip tool installed in your system. Below is the command to install all the necessary libraries required to run the project.

    pip install scrapy
    pip install numpy
    pip install matplotlib
    pip install requests



**Execute below command to crawl the website**

    scrapy crawl debate_crawler -o data.json

**Execute below command to generate histogram**

    python plot.py

**Implementation Strategy**

* Initially, we extracted the URL of the `Popular opinions` webpage and extracted the URLS of *top 5* popular debates
 using ```response.css('.a-image-contain')```.
* We iterated over each URL and extracted the the `Topic` and `Category`.
* We created a list of `yes` and `no` arguments by scraping the data from the first page of the topic.
* Then we checked for the presence of button holder which has the name "Load more arguments".
* If no button is present, i.e., topic has only one page, we just return the first page contents in JSON format.
* If a button is found, then we iterate each and every page starting from `page 2` using `POST` request.
* Since, scrapy doesn't provide response immediately, we had to switch to `requests` library which is an in-built
 libary in Python.
* We're extracting the debate ID from one of the `li` tag in the first page and sending 
```json
{'debateId': str(debate_id), 'pageNumber': page, 'itemsPerPage': 10, 'ysort': 5, 'nsort': 5}
``` 
as POST request body and 
```json
{'content-type': "application/json"}
``` 
as headers as the API available provides JSON string as a response.
* The JSON response after the POST request contains the `HTML` code of the provide `page` with respect to it's debate
 ID as a value to the key `d`.
* We'll parse this JSON response and check if this is the last page by checking whether `HTML` code has `{ddo.split}{ddo.split}finished` as this indicates that there are no more pages ahead.
* We observed that the arguments in the response are splitted by `{ddo.split}` so we append all the arguments before
 this split in the `yes` list and all the arguments after in `no` list.
* When we get the last pages, we just yield the contents in JSON format.
* This happens for each and every top 5 topics.

**Implementation Details**
* ###### `start_request`
 This method is automatically called by scrapy which yields the request object. Once, the
 response is received, calls the `callback` method `parse_main_url`.
 
```python
    def start_requests(self):
        """Call the debates.org website"""
        # predefined pages to crawl
        urls = ['https://www.debate.org/opinions/?sort=popular']
        for url in urls:
            request = scrapy.Request(url=url, callback=self.parse_main_url)
            yield request
```

* ###### `parse_main_url`
 This method receives the object `response` as a callback. The list of all the URLs on the popular page is extracted
  using ```response.css('.a-image-contain')```. We only iterate for the top 5 topic URLs and append them with the
   base url. The generated url is then requested and the respective response is received as a `callback` in the
    method `parse_secondary_urls`.
```python
def parse_main_url(self, response):
        """Returns the object of URLs or top 5 popular opinions"""
        pop_urls_list = response.css('.a-image-contain')
        for i in range(5):  # top 5 popular opinions
            url = pop_urls_list[i].xpath('@href').extract()[0]
            final_url = response.request.url.split('/opinions')[0] + url
            request = scrapy.Request(url=final_url, callback=self.parse_secondary_urls)
            yield request
```


* ###### `parse_secondary_urls`
  - This method receives the object `response` of the popular URL as a callback. 
  - We extract the topic from `h1 ::text` and category from `#breadcrumb a`. 
  - We then create the `l_yes` list by extracting the "yes" arguments using `#yes-arguments li` having the class
   `hasData`.
  - Similar process is repeated for `l_no` list for "no" arguments.
  - The 'title' and the 'body' of each argument is extracted using ```parse_title_body``` method. 
  - We then extract the button holder from `.debate-more-holder`. 
  - If there is no button, we directly yield the `json_dict` otherwise we iterate to each page from `page = 2`.
  - The method `call_more_arguments` is used for simulating the functionality of "Load More Arguments" button and
   returns the output as a string and is stored in `html_str` variable.
  - The condition `if html_str == '{ddo.split}{ddo.split}finished'` checks whether there are more pages ahead or not.
  - If there are still more pages, `extract_more_arguments` is called otherwise the `json_dict` is yielded.
```python
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
```


* ###### `parse_title_body`
  - This method returns a list of `title` and `body` of the arguments based on what type of argument it has received
   as the input, i.e, negative or positive arguments. 
  - The `title` is extracted from `h2 ::text` and `body` is extracted using `p ::text`.
```python
    def parse_title_body(args):
        list_headers = []
        for arguments in args:
            h2_tags = arguments.css('h2 ::text').getall()
            p_tags = arguments.css('p ::text').getall()
            comment = ""
            for txt in p_tags:
                comment += txt
            list_headers.append({"title": h2_tags[0], "body": comment})
        return list_headers
```


* ###### `call_more_arguments`
  - This method takes the `page` number and the `response` of the main page which contains "page 1" of the topic
   and returns `html_str` which is the "value" from JSON response after calling the `POST` method on the `post_url`.   
  - The method send the `str_json` as a `POST` request body to the `post_url`.
  - The response is in the JSON format (because of the `headers`) which contains the HTML code of the requested
   `pageNumber` and `debateID` as a value to the key `d`. 
```python
    def call_more_arguments(page, response):
        post_url = 'https://www.debate.org/opinions/~services/opinions.asmx/GetDebateArgumentPage'
        headers = {'content-type': "application/json"}
        debate_id = response.css('#yes-arguments li')[0].xpath('@did').extract()[0]
        str_json = {'debateId': str(debate_id), 'pageNumber': page, 'itemsPerPage': 10, 'ysort': 5, 'nsort': 5}
        post_body = json.dumps(str_json)
        res = requests.request(method='POST', url=post_url, headers=headers, data=post_body)
        html_str = json.loads(res.text)['d']
        return html_str
```


* ###### `extract_more_arguments`
  - This method takes the `html_str` from `call_more_arguments` method, `l_no` list and `l_yes` list which contains
   the "no" and "yes" arguments of the first page of the topic respectively. 
  - The method extract the arguments after they are splitted using `html_str.split('{ddo.split}')`.  
  - Further extraction of "positive"/"yes" and "negative"/"no" arguments are done using `extract_positive_args` and
   `extract_negative_args` respectively. 
```python
    def extract_more_arguments(self, html_str, l_no, l_yes):
        """Extract the arguments after they are loaded."""
        pos_neg_atr_list = html_str.split('{ddo.split}')
        self.extract_positive_args(l_yes, pos_neg_atr_list)
        self.extract_negative_args(l_no, pos_neg_atr_list)
```


* ###### `extract_negative_args` and `extract_positive_args`
  - These methods takes the `l_no` and `l_yes` respectively along with `pos_neg_atr_list` from
   `extract_more_arguments` method to separate the positive and negative arguments in the extra loaded arguments. 
  - The methods extract the arguments from the `li` tags having `hasData` class.   
```python
    def extract_negative_args(self, l_no, pos_neg_atr_list):
        neg_html = pos_neg_atr_list[1]
        neg_selector = scrapy.Selector(text=neg_html)
        neg_args = neg_selector.css('li').css('.hasData')
        list_neg_li_tags = self.parse_title_body(neg_args)
        l_no.extend(list_neg_li_tags)

    def extract_positive_args(self, l_yes, pos_neg_atr_list):
        pos_html = pos_neg_atr_list[0]
        pos_selector = scrapy.Selector(text=pos_html)
        pos_args = pos_selector.css('li').css('.hasData')
        list_pos_li_tags = self.parse_title_body(pos_args)
        l_yes.extend(list_pos_li_tags)

```

* Once we have the data.json file which contains the extracted data, we plot *histogram* (<span style="color:red">*plot.py*</span>) to analyse the extracted data. We iterate the data for every topic and store the number of arguments per topic *(num_args)* which includes the pro arguments and the con arguments in the dictionary *hist_per_topic*. 

```python
num_args = len(json_data[topic]['pro_arguments']) + len(json_data[topic]['con_arguments'])
hist_per_topic[json_data[topic]['topic']] = num_args
```

* For every topic we store the length of each pro argument and each con argument in the list *hist_per_argument_length*. So the final list will contain the length of all the arguments for all the topics. 
```python
# Store the length of each pro argument
for pro_args in range(0, len(json_data[topic]['pro_arguments'])):
    hist_per_argument_length.append(len(json_data[topic]['pro_arguments'][pro_args]['body']))

# Store the length of each con argument
for con_args in range(0, len(json_data[topic]['con_arguments'])):
    hist_per_argument_length.append(len(json_data[topic]['con_arguments'][con_args]['body']))
```


* To store the number of arguments per category, we first check if the category of the iterated topic is already stored in the dictionary *hist_per_category*. If it is not present we store the key i.e., the category and the value i.e., the number of arguments in the dictionary. If the category is already present we just add to the current number of arguments to the key value. 

```python
if json_data[topic]['category'] in hist_per_category.keys():
    hist_per_category[json_data[topic]['category']] = hist_per_category.get(json_data[topic]['category']) + num_args
else:
    hist_per_category[json_data[topic]['category']] = num_args
```
