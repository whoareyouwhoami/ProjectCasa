# Test Script
import time
import logging
from urllib.parse import urlparse
import pandas as pd
import run_log
import collect as WebCrawl

logger = logging.getLogger('run_log')

class CrawlTest:
    def __init__(self, unit_all=False, driver_type='chrome',url=None):
        if unit_all is False and url is None:
            raise ValueError("URL required")

        logger.debug('----------------- TEST RUN -----------------')

        self.url = url
        self.initiate = WebCrawl.Initiate()
        self.landsite = WebCrawl.WebCrawling()
        self.driver = self.initiate.OpenDriver(type=driver_type)

        if unit_all is False:
            self.landsite.web_open(driver=self.driver, url=self.url)

    def unit_apartment_name(self, start, end):
        if end < 1 or start < 1:
            raise ValueError('Input value should be higher than 1')
        if start > end:
            raise ValueError('Starting page should be lesser than ending page')

        file = pd.read_csv('apartment_url.csv', encoding='euc-kr')
        url_list = list(file['url'][start - 1:end])
        x = start
        for idx, url in enumerate(url_list):
            logger.debug('URL: ' + str(x))
            logger.debug(str(url))

            url_parse = urlparse(url)
            # Apartment ID
            url_id = url_parse.path.split('/')[-1]

            self.landsite.web_open(driver=self.driver, url=str(url))
            self.landsite.web_collect_name(url_id=url_id, id=idx)

            x += 1

    def unit_all(self, start, end):
        if end < 1 or start < 1:
            raise ValueError('Input value should be higher than 1')
        if start > end:
            raise ValueError('Starting page should be lesser than ending page')

        try:
            file = pd.read_csv('apartment_url.csv', encoding='euc-kr')
        except FileNotFoundError:
            print('Please run `web_collectURL()` or place `apartment_url.csv` where testing script exist)')
            return False

        url_list = list(file['url'][start - 1:end])
        x = start
        for idx, url in enumerate(url_list):
            print('\nURL:', str(x))
            print(str(url))

            url_parse = urlparse(url)
            # Apartment ID
            url_id = url_parse.path.split('/')[-1]

            self.landsite.web_open(driver=self.driver, url= str(url))
            self.landsite.web_collect(url_id=url_id, id=idx)

            x += 1

    def unit_collectURL(self):
        self.landsite.web_collectURL()

test = CrawlTest(unit_all=True, driver_type='firefox', url='https://new.land.naver.com/complexes/1?ms=37.548119,127.040638,17&a=APT:JGC:ABYG&e=RETAIL')
# test.unit_collectURL()
# test.unit_all(start=869, end=869)
test.unit_apartment_name(start=110, end=8029)