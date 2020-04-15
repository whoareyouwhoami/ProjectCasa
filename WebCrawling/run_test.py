# Test Script
import time
import pandas as pd
import collect as WebCrawl

class CrawlTest:
    def __init__(self, unit_all=False, url=None):
        if unit_all is False and url is None:
            raise ValueError("URL required")

        self.url = url
        self.initiate = WebCrawl.Initiate()
        self.landsite = WebCrawl.WebCrawling()
        self.driver = self.initiate.OpenDriver()

        if unit_all is False:
            self.landsite.web_open(driver=self.driver, url=self.url)

    def unit_initiate(self):
        apartment_info = self.driver.find_element_by_xpath("/html/body/div[2]/div/section/div[2]/div[1]/div/div/div[1]/div[1]/div[2]/div[2]/button[1]")
        apartment_info.click()
        time.sleep(1)

    def unit_apartment(self):
        self.landsite._apartment_info()

    def unit_school(self):
        self.unit_initiate()
        self.landsite._school_info()

    def unit_tower(self):
        self.unit_initiate()
        item_list = self.landsite._apartment_filter()
        if item_list:
            self.landsite._tower_info(items=item_list[0])
            # for item in item_list:
            #     self.landsite._tower_info(items=item)

    def unit_all(self, start, end):
        if end < 1 or start < 1:
            raise ValueError('Input value should be higher than 1')
        if start > end:
            raise ValueError('Starting page should be lesser than ending page')

        end += 1

        try:
            file = pd.read_csv('apartment_url.csv', encoding='euc-kr')
        except FileNotFoundError:
            print('Please run `web_collectURL()` or place `apartment_url.csv` where testing script exist)')
            return False

        url_list = list(file['url'][start:end])

        for idx, url in enumerate(url_list):
            print('\nURL:', str(idx))

            self.landsite.web_open(driver=self.driver, url=str(url))
            self.landsite.web_collect()

    def unit_collectURL(self):
        self.landsite.web_collectURL()

test = CrawlTest(unit_all=True, url='https://new.land.naver.com/complexes/1?ms=37.548119,127.040638,17&a=APT:JGC:ABYG&e=RETAIL')
# test.unit_apartment()
# test.unit_school()
# test.unit_tower()
test.unit_all(start=1, end=2)
# test.unit_collectURL()