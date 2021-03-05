import scrapy

from scrapy.loader import ItemLoader
from w3lib.html import remove_tags

from ..items import NlbrsItem
from itemloaders.processors import TakeFirst


class NlbrsSpider(scrapy.Spider):
	name = 'nlbrs'
	start_urls = ['https://www.nlb.rs/index.php?go=strana&ID=16911&jezik=lat&year=sve&q=Pretra%C5%BEi+po+sadr%C5%BEaju']

	def parse(self, response):
		post_links = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "link", " " ))]//a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "holder", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "ckeditor", " " ))]//strong/text()').get()
		description = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "bela-podlaga", " " )) and (((count(preceding-sibling::*) + 1) = 4) and parent::*)]//*[contains(concat( " ", @class, " " ), concat( " ", "holder", " " ))]').getall()
		description = [remove_tags(p).strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "ae_datum", " " ))]/text()').get()

		item = ItemLoader(item=NlbrsItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
