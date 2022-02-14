import scrapy
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
import time

class CoinSpider(scrapy.Spider):
    name = 'coin'

    def start_requests(self):
        yield SeleniumRequest(
            url='https://coinmarketcap.com/',
            wait_time=3,
            callback=self.parse
        )

    def parse(self, response):
        driver = response.meta['driver']

        for n in range(4):
            time.sleep(3)
            driver.execute_script("window.scrollTo(0, window.scrollY + 2080)")

        html = driver.page_source
        response_obj = Selector(text=html)

        names = response_obj.xpath("//table/tbody/tr/td[3]/div/a/div/div/p")
        imgs = response_obj.xpath("//table/tbody/tr/td[3]/div/a/div/img")
        prices = response_obj.xpath("//table/tbody/tr/td[4]/div/a/span")

        count = len(names)

        for x in range(count):
            name = names[x].xpath(".//text()").get()
            img = imgs[x].xpath(".//@src").get()
            price = prices[x].xpath(".//text()").get()

            yield {
                'name': name,
                'img': img,
                'price': price
            }