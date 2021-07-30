import scrapy

class Places_Spider(scrapy.Spider):
    name = 'places'
    start_urls = [
        'https://www.nationalgeographic.com/environment'
    ]

    def parse(self, response):
        article_links = response.css('.PromoTile__Link').xpath('@href').extract() 