# to run 
# scrapy crawl imdb_spider -o movies.csv
import scrapy

class ImdbSpider(scrapy.Spider):
    name = 'imdb_spider'
    start_urls = ['https://www.imdb.com/title/tt0106145/']

    def parse(self, response):
        cast_page = response.url + 'fullcredits/'
        yield scrapy.Request(cast_page, self.parse_full_credits)

    def parse_full_credits(self, response):
        actor_lists = [a.attrib["href"] for a in response.css("td.primary_photo a")]
        for ele in actor_lists:
            actor_page = 'https://www.imdb.com' + ele
            yield scrapy.Request(actor_page, self.parse_actor_page)
    
    def parse_actor_page(self, response):
        actor_name = response.css('title::text')[0].get().split(' -')[0]
        title_lists = response.css("div.filmo-row[id^=act]")
        for movie_or_TV_name in title_lists:
            yield{"actor" : actor_name, "movie_or_TV_name" : movie_or_TV_name.css("a::text").get()}


