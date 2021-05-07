# Computational Argumentation Assignment No 1 
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
├── Bar_Graph_Num_arg_per_category.png
├── Bar_Graph_Num_arg_per_topic.png
├── documentation
├── Hist_per_argument_length.png
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

    TO BE ADDED


**Implementation Details**

*  We use Scrapy framework for **data acquisation**. Scrapy is a fast high-level web crawling and web scraping framework that allows you crawl websites and extract structure data from web pages. 
* The most import component here are the spiders where you specify the rules of how a certain site will be scraped, including how to perform the crawl and how to extract data from the it.
* In our implementaion (<span style="color:red">*my_spider.py*</span>), we specify the website to be crawled in the function *start_request*. This function inturn calls a callback function *parse_main_url* using which we extract the top 5 populat opinions from the response.

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
* Write here the remaining code details

```python
print("Not yet written")
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
