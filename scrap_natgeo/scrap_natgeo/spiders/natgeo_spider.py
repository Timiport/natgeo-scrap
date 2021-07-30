import scrapy
from scrap_natgeo.items import ScrapNatgeoItem

class Natgeo_Spider(scrapy.Spider):
    name = 'natgeo'
    start_urls = [
        'https://www.nationalgeographic.com/environment'
    ]

    def parse(self, response):
        article_links = response.css('.PromoTile__Link::attr(href)').extract()
        # print(article_links)
        for link in article_links:
            yield response.follow(link, callback=self.parse_content)
            # yield {link: 1}

    def parse_content(self, response):
        items = ScrapNatgeoItem()
        title = response.css('title::text').extract()
        content = response.css('p::text').extract()

        items['title'] = title
        items['content'] = ' '.join(content)

        yield items