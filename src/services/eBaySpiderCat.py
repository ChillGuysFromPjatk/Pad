import scrapy
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerProcess

class EbayScraperItem(scrapy.Item):
    model = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    condition = scrapy.Field()
    seller = scrapy.Field()
    sale_date = scrapy.Field()
    country = scrapy.Field()

class eBaySpider(scrapy.Spider):
    allowed_domains = ["ebay.pl"]
    name = 'eBaySpider'

    consoles = ['Microsoft Xbox', 'Microsoft Xbox 360', 'Microsoft Xbox 360 Arcade', 'Microsoft Xbox 360 Core', 'Microsoft Xbox 360 E', 'Microsoft Xbox 360 Elite', 
                'Microsoft Xbox 360 Premium', 'Microsoft Xbox 360 Pro', 'Microsoft Xbox 360 S', 'Microsoft Xbox One', 'Microsoft Xbox One S', 'Microsoft Xbox One X',
                'Microsoft Xbox Series S', 'Microsoft Xbox Series X', 'New Nintendo 2DS XL', 'New Nintendo 3DS', 'New Nintendo 3DS LL', 'New Nintendo 3DS XL',
                'Nintendo 2DS', 'Nintendo 2DS LL', 'Nintendo 3DS', 'Nintendo 3DS XL', 'Nintendo 64', 'Nintendo DS', 'Nintendo DSi', 'Nintendo DSi XL', 'Nintendo DS Lite',
                'Nintendo Game Boy', 'Nintendo Game Boy Advance', 'Nintendo Game Boy Advance SP', 'Nintendo Game Boy Color', 'Nintendo Game Boy Light', 'Nintendo Game Boy Micro',
                'Nintendo Game Boy Pocket', 'Nintendo GameCube', 'Nintendo NES', 'Nintendo NES Classic Edition', 'Nintendo SNES', 'Nintendo Super NES Classic Edition',
                'Nintendo Switch', 'Nintendo Switch (OLED Model)', 'Nintendo Switch Lite', 'Nintendo Wii', 'Nintendo Wii mini', 'Nintendo Wii U - Basic', 'Nintendo Wii U - Deluxe',
                'Sony PlayStation 1', 'Sony PlayStation 2', 'Sony PlayStation 2 - Slim', 'Sony PlayStation 3', 'Sony PlayStation 3 - Slim', 'Sony PlayStation 3 - Super Slim',
                'Sony PlayStation 4', 'Sony PlayStation 4 Pro', 'Sony PlayStation 4 Slim', 'Sony PlayStation 5 Blu-Ray Edition', 'Sony PlayStation 5 Digital Edition', 
                'Sony PlayStation 5 Slim Blu-Ray Edition', 'Sony PlayStation 5 Slim Digital Edition', 'Sony PlayStation Classic', 'Sony PlayStation Portable', 'Sony PSP-1000',
                'Sony PSP-1001', 'Sony PSP-2000', 'Sony PSP-3000', 'Sony PSP-3001', 'Sony PSP-E1000', 'Sony PS Vita - PCH-1000', 'Sony PS Vita - PCH-1001', 'Sony PS Vita - PCH-1101', 
                'Sony PS Vita - PCH-2000', 'Sony PS Vita PCH-2001', 'Valve Steam Deck']
    
    def start_requests(self):
        base_url = "https://www.ebay.pl/sch/Gry-i-Konsole/139971/i.html?_fsrp=1&_sacat=139971&LH_Sold=1&_ipg=240&_oaa=1&_dcat=139971&Model={model}&_pgn={page}"
        for model in self.consoles:
            model_link = model.replace(' ', '%2520').replace('-', '%252D').replace('(', '%2528').replace(')', '%2529')
            url = base_url.format(model=model_link, page=1)
            yield scrapy.Request(url, callback=self.parse, meta={'model': model, 'page': 1})
            
    def parse(self, response):
        model = response.meta['model']
        page = response.meta['page']

        self.logger.info(f"Parsing page {page} for model {model}")

        listings = response.xpath('//li[contains(@class, "s-item")]')
        self.logger.info(f"Found {len(listings)} listings on page {page}")
        
        for listing in listings:
            loader = ItemLoader(item=EbayScraperItem(), selector=listing)
            
            loader.add_value('model', model)
            loader.add_xpath('title', './/a[@class="s-item__link"]//div[@class="s-item__title"]/span[@role="heading"]/text()')
            loader.add_xpath('price', './/div[@class="s-item__detail s-item__detail--primary"]/span[@class="s-item__price"]/span[@class="POSITIVE ITALIC"]/text()')
            loader.add_xpath('condition', './/span[contains(@class, "SECONDARY_INFO")]/text()')
            loader.add_xpath('seller', './/span[contains(@class, "s-item__seller-info-text")]/text()')
            loader.add_xpath('sale_date', './/div[contains(@class, "s-item__caption")]//span[contains(text(), "Sprzedane")]/text()')
            loader.add_xpath('country', './/div[@class="s-item__detail s-item__detail--primary"]/span[@class="s-item__location s-item__itemLocation"]/span[@class="ITALIC"]/text()')
            
            yield loader.load_item()
        
        next_page_url = response.xpath('//a[contains(@class, "pagination__next")]/@href').get()
        if next_page_url:
            self.logger.info(f"Found next page for model {model}: {next_page_url}")
            yield scrapy.Request(next_page_url, callback=self.parse, meta={'model': model, 'page': page + 1})
        else:
            self.logger.info(f"No more pages for model {model} at page {page}")

process = CrawlerProcess(settings={
    "FEEDS": {
        "output_ebayspidercat_2.csv": {"format": "csv"},
    },
    "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.92 Safari/537.36",
    "LOG_LEVEL": "INFO",
    "HTTPCACHE_ENABLED": False,
    "DOWNLOAD_DELAY": 2,
    "RANDOMIZE_DOWNLOAD_DELAY": True,
    "ROBOTSTXT_OBEY": False,
})
process.crawl(eBaySpider)
process.start()