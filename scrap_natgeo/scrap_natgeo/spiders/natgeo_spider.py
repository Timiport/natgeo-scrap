import scrapy
import pyjson5
from scrap_natgeo import settings
from scrap_natgeo.items import ScrapNatgeoItem

class Natgeo_Spider(scrapy.Spider):
    name = 'natgeo'
    start_urls = [
        f'https://www.nationalgeographic.com/{settings.TOPIC}'
    ]
    article_links = []
    have_next_page = True
    context=''
    page = 1
    def parse(self, response):
        
        next_page, id_num = '', ''
        
       
        
        next_page = response.css('script::text')[1].extract()
        page_info = next_page[next_page.rfind('id', 0, next_page.index('InfiniteFeedModule'))-1:]
        page_info = '{' + page_info[:page_info.rfind(',', 0, page_info.index('"tiles"')-1)]
        # print(page_info)
        page_dict = pyjson5.decode(page_info)
        
        id_num = page_dict['id']
        next_page = page_dict['pageInfo']['endCursor']
        have_next_page = page_dict['pageInfo']['hasNextPage']
        self.context = page_dict['templateContext']


        self.article_links = response.css('.PromoTile__Link::attr(href)').extract()
        
        next_page_url = f'https://www.nationalgeographic.com/proxy/hub?after={next_page}&context={self.context}&id={id_num}&moduleType=InfiniteFeedModule&_xhr=pageContent'

        yield response.follow(next_page_url, callback=self.parse_more_content)

    def parse_more_content(self, response):
        if self.have_next_page and self.page < settings.MAX_PAGE:
            self.page += 1
            next_page_json = pyjson5.decode(response.text)
            
            article_list = next_page_json['tiles']
            for article in article_list: 
                self.article_links.append(article['ctas'][0]['url'])
        
            self.have_next_page = next_page_json['pageInfo']['hasNextPage']
            id_num = next_page_json['id']
            next_page = next_page_json['pageInfo']['endCursor']
            
            next_page_url = f'https://www.nationalgeographic.com/proxy/hub?after={next_page}&context={self.context}&id={id_num}&moduleType=InfiniteFeedModule&_xhr=pageContent'
            
            yield response.follow(next_page_url, callback=self.parse_more_content)

       
        for link in self.article_links:
            
            yield response.follow(link, callback=self.parse_content)
       

    def parse_content(self, response):
        items = ScrapNatgeoItem()
        title = response.css('title::text').extract()
        content = response.css('p::text').extract()

        items['title'] = title
        items['content'] = ' '.join(content)

        yield items