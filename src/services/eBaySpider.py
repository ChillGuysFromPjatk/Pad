from typing import Any

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.http import Response
from scrapy_playwright.page import PageMethod


class eBaySpider(scrapy.Spider):
    name = 'eBaySpider'

    def start_requests(self):
        for page in range(1, 160):
            url = f'https://www.ebay.pl/sch/i.html?_dcat=1249&_fsrp=1&_sacat=1249&LH_Complete=1&LH_Sold=1&Model=PlayStation%25204%2520Slim%7CPlayStation%25204%2520Pro%7CPlayStation%25204%2520%252D%2520Original&_pgn={page}&rt=nc'
            self.log(f"Queuing URL: {url}")
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response: Response, **kwargs: Any) -> Any:
        self.log(f"Scraping URL: {response.url}")
        products = response.css("div.s-item__info.clearfix")
        self.log(f"Found {len(products)} products on {response.url}")

        if not products:
            self.log(f"No products found on {response.url}.")
            with open(f"empty_page_{response.url.split('=')[-1]}.html", "wb") as f:
                f.write(response.body)

        for product in products:
            yield self._parse_item(product)

    def _parse_item(self, product: scrapy.Selector) -> dict:
        item = {
            "name": product.css("a.s-item__link div.s-item__title span::text").get(default="N/A").strip(),
            "sold_date": product.css("div.s-item__caption span.s-item__caption--signal.POSITIVE span::text").get(
                default="N/A").strip(),
            "price": product.css("span.s-item__price span.POSITIVE.ITALIC::text").get(default="N/A").strip(),
            "seller_country": product.css("span.s-item__location.s-item__itemLocation span::text").get(default="N/A").strip(),
            "seller_name": product.css(
                "span.s-item__seller-info-text span::text, span.s-item__seller-info-text::text").get(
                default="N/A").strip(),
            "product_condition": product.css("span.SECONDARY_INFO::text").get(default="N/A").strip(),
        }
        return item


process = CrawlerProcess(settings={
    "FEEDS": {
        "output_spider.csv": {"format": "csv"},
    },
"USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.92 Safari/537.36",
    "HTTPCACHE_ENABLED": False,
    "DOWNLOAD_DELAY": 2,
    "RANDOMIZE_DOWNLOAD_DELAY": True,
    "ROBOTSTXT_OBEY": False,

})
process.crawl(eBaySpider)
process.start()
