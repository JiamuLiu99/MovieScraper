# to run 
# scrapy crawl imdb_spider -o movies.csv
import scrapy

class ImdbSpider(scrapy.Spider):
    name = 'imdb_spider'
    start_urls = ['https://www.imdb.com/title/tt6450804/']  # Terminator: Dark Fate

    # head to cast listing page and call [parse_full_credits]
    def parse(self, response):
        yield scrapy.Request(response.url + 'fullcredits/', self.parse_full_credits)

    # head to actor page and call [parse_actor_page]
    def parse_full_credits(self, response):
        # read all actors' links at current page
        actor_lists = [a.attrib["href"] for a in response.css("td.primary_photo a")]
        for ele in actor_lists:
            # head to each actor's page and call [parse_actor_page]
            yield scrapy.Request('https://www.imdb.com' + ele, self.parse_actor_page)
    
    def parse_actor_page(self, response):
        # read actor name
        actor_name = response.css('title::text')[0].get().split(' -')[0]
        # read filmography
        title_lists = response.css("div.filmo-row[id^=act]")
        for movie_or_TV_name in title_lists:
            # save data to .csv
            yield{"actor" : actor_name, "movie_or_TV_name" : movie_or_TV_name.css("a::text").get()}
