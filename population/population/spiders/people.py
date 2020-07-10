# -*- coding: utf-8 -*-
import scrapy


class PeopleSpider(scrapy.Spider):
    name = 'people'
    allowed_domains = ['www.worldometers.info']
    start_urls = ['https://www.worldometers.info/world-population/population-by-country/']

    def parse(self, response):
        
        countries = response.xpath("////td/a")

        for c in countries:
            
            name = c.xpath(".//text()").get()
            link = c.xpath(".//@href").get()

            yield response.follow(url = link, callback = self.single_country, meta = {"name":name})
    
    def single_country(self, response):

        country = response.request.meta["name"]
        rows = response.xpath("(//table[@class='table table-striped table-bordered table-hover table-condensed table-list'])[1]/tbody/tr")

        for r in rows:

            year = r.xpath(".//td[1]/text()").get()
            people = r.xpath(".//td[2]/strong/text()").get()

            yield {
                
                "Country": country,
                "Year": year,
                "Population": people

            }

