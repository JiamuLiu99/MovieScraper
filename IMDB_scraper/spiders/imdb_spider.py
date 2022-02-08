# to run 
# scrapy crawl imdb_spider -o movies.csv
import scrapy

class ImdbSpider(scrapy.Spider):
    name = 'imdb_spider'
    start_urls = ['https://www.imdb.com/title/tt6450804/']  # Terminator: Dark Fate

    def parse(self, response):
        """
        Assuming the start_urls is correctly loaded with a movie introduction page, this method
        will navigate to casts listing(Cast & Crew) page(<movie_url>fullcredits)
        and call [parse_full_credits(self, response)] through yield.

        return: NULL
        """
        yield scrapy.Request(response.url + 'fullcredits/', self.parse_full_credits)

    def parse_full_credits(self, response):
        """
        Assuming the Cast & Crew page is loaded correctly, this method
        will retrieve each actor listed on current page and call [parse_actor_page(self, response)]
        through yield.

        return: NULL
        """
        # read all actors' links at current page
        actor_lists = [a.attrib["href"] for a in response.css("td.primary_photo a")]
        for ele in actor_lists:
            # read each actor's page and call [parse_actor_page(self, response)]
            yield scrapy.Request('https://www.imdb.com' + ele, self.parse_actor_page)
    
    def parse_actor_page(self, response):
        """
        Assuming each actor's page is loaded successfully, this method will retrieve
        each actor's name and his or her movies. Then, bind their name and each movie name
        and write to .csv file by using yield.
        """
        # read actor name
        actor_name = response.css('title::text')[0].get().split(' -')[0]
        # read filmography
        title_lists = response.css("div.filmo-row[id^=act]")
        for movie_or_TV_name in title_lists:
            # save data to .csv
            yield{"actor" : actor_name, "movie_or_TV_name" : movie_or_TV_name.css("a::text").get()}
