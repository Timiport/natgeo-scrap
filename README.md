# natgeo-scrap
A scrapy program to scrapy articles from Nation Geography

## Requirement
Install scrapy using `pip install scrapy`\
Install json5 using `pip install pyjson5`

## Get Started
Switch directory with `cd scrap_natgeo`. \
In the command line, run `scrapy crawl natgeo -o result.json`. This will execute scrapy and crawl the articles.

## Settings
There are two settings you could modify, which can be found in `scrap_natgeo/scrap_natgeo/settings.py`. 
* MAX_PAGE: the number of pages you want to crawl
* TOPIC: the topic you want to crawl, such as 'environment', 'animals', 'history' and etc. 
  * These should match with the National Georgraphy's url extension. 
  * For example, a url here is https://www.nationalgeographic.com/science, in this case, the extension here should be *science*, which is the topic you should put.

## Results
The result will be in a form of json file with the format
```
{
  "title": "...", 
  "content": "..."
}
```
Which `content` is the content of the article

## More works
National Geography did not use pagination, and instead uses a *load more* button to send network information and query a javascript containing all the necessary information, including article links, picture urls, and more. This crawler provide a general functionality to follow through National Geography's procedurally generated query url.

If you wish to add more functionality to this crawler, like if you want to crawl article pictures, feel free to look at `example javascript.txt` at the root to see what kind of data there is that you could process. 
