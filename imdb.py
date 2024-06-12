import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class ImdbSpider(CrawlSpider):
    name = "imdb"
    allowed_domains = ["m.imdb.com"]
    start_urls = ["https://m.imdb.com/chart/top"]

    rules = (Rule(LinkExtractor(restrict_xpaths='//ul[@class="ipc-metadata-list ipc-metadata-list--dividers-between sc-a1e81754-0 eBRbsI compact-list-view ipc-metadata-list--base"]/li//a[@class="ipc-title-link-wrapper"]'), callback="parse_item", follow=True),)

    def parse_item(self, response):
        genres = response.xpath('//div[@data-testid="genres"]//a//text()')
        movie_name = response.xpath('//span[@class="hero__primary-text"]/text()')
        ratings = response.xpath('//div[@data-testid="hero-rating-bar__aggregate-rating__score"]/span/text()')
        year = response.xpath('//ul[@class="ipc-inline-list ipc-inline-list--show-dividers sc-d8941411-2 cdJsTz baseAlt"]/li[1]//text()')
        duration = response.xpath('//ul[@class="ipc-inline-list ipc-inline-list--show-dividers sc-d8941411-2 cdJsTz baseAlt"]/li[3]//text()')
        num_of_ratings = response.xpath('//div[@data-testid="hero-rating-bar__aggregate-rating__score"]/following-sibling::div[2]//text()')
        yield{
            "Name":movie_name.get(),
            "Release_Date":year.get(),
            "Duration":duration.get(),
            "Genres": genres.getall(),
            "Rating":ratings.get(),
            "Num_of_Ratings":num_of_ratings.get(),
            # "url":response.url,
        }

