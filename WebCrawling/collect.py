##################################
#      Web Crawling Script
##################################
import os
import time
import pandas as pd
from selenium import webdriver as wd
from selenium.webdriver.chrome.options import Options

# Display options
pd.set_option("display.max_columns", 2000)
pd.set_option("display.width", 1000)
pd.set_option("display.max_rows", 1000)

# Driver options
chrome_options = Options()
chrome_options.add_argument("--headless")

class Initiate:
    def __init__(self):
        self.root = os.path.realpath(os.pardir)
        self.current = os.path.dirname(os.path.realpath(__file__))
        self.chrome_driver = os.path.join(self.current, 'chromedriver')

    def OpenDriver(self):
        self.driver = wd.Chrome(self.chrome_driver) # options=chrome_options
        return self.driver

class WebCrawling:
    def __init__(self):
        self.name = 'hello world'

    def web_open(self, driver, url=None):
        if url is None:
            raise ValueError("URL required.")

        self.driver = driver
        self.url = url
        self.driver.get(self.url)

    def web_verify(self):
        city = self.driver.find_element_by_css_selector("span.area:nth-child(2)")
        print(city.text)
        return True

        # if city.text == '서울시':
        #     return True
        # else:
        #     return False

    def web_collect(self):
        item_list = self._apartment_filter()

        if not item_list:
            print('Empty list')
            return False

        self._apartment_info()
        self._school_info()
        self._tower_info(items=item_list)

    def _apartment_filter(self):
        # Choosing method
        choice_lst = self.driver.find_element_by_xpath("/html/body/div[2]/div/section/div[2]/div[1]/div/div/div[1]/div[2]/div/div[1]/button")
        choice_lst.click()
        time.sleep(1)

        # Choose buy
        buy = self.driver.find_element_by_xpath("/html/body/div[2]/div/section/div[2]/div[1]/div/div/div[1]/div[2]/div/div[1]/div/div/ul/li[2]")
        buy.click()
        time.sleep(1)

        # Apartment list
        try:
            initial_items = self.driver.find_elements_by_xpath("/html/body/div[2]/div/section/div[2]/div[1]/div/div/div[2]/div/div/div[5]/div/a[2]/div[1]/span[2]")
            initial_len = len(initial_items)
        except:
            return []

        # Extending list
        while True:
            scroll = self.driver.find_element_by_xpath('/html/body/div[2]/div/section/div[2]/div[1]/div/div/div[2]/div')
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scroll)

            time.sleep(1.5)

            items = self.driver.find_elements_by_xpath("/html/body/div[2]/div/section/div[2]/div[1]/div/div/div[2]/div/div/div/div/a")
            items_len = len(items)

            if initial_len != items_len:
                initial_len = items_len
            else:
                self.driver.execute_script("arguments[0].scrollTop = 0", scroll)
                return items

    def _apartment_info(self):
        apartment_info = self.driver.find_element_by_xpath("/html/body/div[2]/div/section/div[2]/div[1]/div/div/div[1]/div[1]/div[2]/div[2]/button[1]")
        apartment_info.click()
        time.sleep(1)

        apartment_built = self.driver.find_element_by_css_selector(".detail_box--complex > table:nth-child(3) > tbody:nth-child(2) > tr:nth-child(2) > td:nth-child(2)").text
        apartment_builder = self.driver.find_element_by_css_selector(".detail_box--complex > table:nth-child(3) > tbody:nth-child(2) > tr:nth-child(4) > td:nth-child(2)").text
        apartment_floor = self.driver.find_element_by_css_selector(".detail_box--complex > table:nth-child(3) > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(4)").text
        apartment_floor_ratio = self.driver.find_element_by_css_selector(".detail_box--complex > table:nth-child(3) > tbody:nth-child(2) > tr:nth-child(3) > td:nth-child(2)").text
        apartment_address = self.driver.find_element_by_css_selector("p.address:nth-child(1)").text
        apartment_parking = self.driver.find_element_by_css_selector("table.info_table_wrap:nth-child(3) > tbody:nth-child(2) > tr:nth-child(2) > td:nth-child(4)").text

        print('Apartment build date:', apartment_built)
        print('Apartment construction company:', apartment_builder)
        print('Apartment floor:', apartment_floor)
        print('Apartment floor ratio:', apartment_floor_ratio)
        print('Apartment parking:', apartment_parking)
        print('Apartment address:', apartment_address)

    def _school_info(self):
        school_info = self.driver.find_element_by_xpath('/html/body/div[2]/div/section/div[2]/div[2]/div/div[2]/div[2]/div/div/a[@id="detailTab4"]')
        school_info.click()
        time.sleep(1)

        school_name = self.driver.find_element_by_xpath('/html/body/div[2]/div/section/div[2]/div[2]/div/div[2]/div[6]/div/div[1]/div[1]/h5').text
        school_dist = self.driver.find_element_by_xpath('/html/body/div[2]/div/section/div[2]/div[2]/div/div[2]/div[6]/div/div[1]/div[2]/div[2]/div[2]').text
        school_address = self.driver.find_element_by_xpath('/html/body/div[2]/div/section/div[2]/div[2]/div/div[2]/div[6]/div/div[1]/table/tbody/tr[1]/td').text
        school_students = self.driver.find_element_by_xpath('/html/body/div[2]/div/section/div[2]/div[2]/div/div[2]/div[6]/div/div[1]/table/tbody/tr[6]/td').text

        print('Nearby school:', school_name)
        print('Time to school:', school_dist)
        print('School address:', school_address)
        print('Number of students:', school_students)

    def _tower_info(self, items):
        if not items:
            return False

        for idx in range(len(items)):
            print("\nList ID:", idx)

            items[idx].click()
            time.sleep(1)

            try:
                tower_id = self.driver.find_element_by_css_selector("tr.info_table_item:nth-child(7) > td:nth-child(2)").text
                int(tower_id)
            except:
                try:
                    tower_id = self.driver.find_element_by_css_selector("tr.info_table_item:nth-child(7) > td:nth-child(4)").text
                except:
                    continue

            tower_head = self.driver.find_element_by_css_selector(".info_title_wrap > h4:nth-child(1)").text
            tower = self.driver.find_element_by_css_selector(".info_title_wrap > h4:nth-child(1) > strong:nth-child(1)").text
            tower_floor = tower_head.replace(tower, '')

            tower_area = self.driver.find_element_by_css_selector(".detail_box--summary > table:nth-child(2) > tbody:nth-child(2) > tr:nth-child(2) > td:nth-child(2)").text
            tower_bathroom = self.driver.find_element_by_css_selector(".detail_box--summary > table:nth-child(2) > tbody:nth-child(2) > tr:nth-child(3) > td:nth-child(4)").text
            tower_household = self.driver.find_element_by_css_selector("tr.info_table_item:nth-child(7) > td:nth-child(2)").text
            tower_floor_mx = self.driver.find_element_by_css_selector(".detail_box--summary > table:nth-child(2) > tbody:nth-child(2) > tr:nth-child(3) > td:nth-child(2)").text

            print('Tower ID:', tower_id)
            print('Tower name:', tower)
            print('Tower bathroom', tower_bathroom)
            print('Tower floor:', tower_floor)
            print('Tower size:', tower_area)
            print('Tower household:', tower_household)
            print('Tower maximum floor:', tower_floor_mx)

            # self._tower_price()

    def _tower_price(self):
        price = self.driver.find_element_by_xpath("/html/body/div[2]/div/section/div[2]/div[2]/div/div[2]/div[1]/div[2]/div/a[@id='detailTab2']")
        price.click()

        # ------------------------------------------
        # consider deleting it later
        # since buying house was selected before
        # ------------------------------------------
        price_buy = self.driver.find_element_by_xpath('//*[@id="marketPriceTab1"]')
        price_buy.click()
        # ------------------------------------------

        see_more = self.driver.find_element_by_xpath("/html/body/div[2]/div/section/div[2]/div[2]/div/div[2]/div[3]/div/div[4]/button")

        try:
            while see_more:
                see_more.click()
                time.sleep(1)

        except Exception as err:
            # delete later
            # print('-- Error --\n', err)
            pass

        rows = self.driver.find_elements_by_xpath("/html/body/div[2]/div/section/div[2]/div[2]/div/div[2]/div[3]/div/div[4]/table/tbody/tr")
        print('Price list:', len(rows))
        # for row in rows:
        #     print(row.text)


