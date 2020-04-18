##################################
#      Web Crawling Script
##################################
import os
import time
import logging
import pandas as pd
from urllib.parse import urlparse, parse_qs
from selenium import webdriver as wd
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import decorators as dc

# Display options
pd.set_option("display.max_columns", 2000)
pd.set_option("display.width", 1000)
pd.set_option("display.max_rows", 1000)

# Driver options
chrome_options = ChromeOptions()
chrome_options.add_argument("--headless")

gecko_options = FirefoxOptions()
gecko_options.add_argument("--headless")

# Log
logger = logging.getLogger('run_log')

class Initiate:
    def __init__(self):
        self.root = os.path.realpath(os.pardir)
        self.current = os.path.dirname(os.path.realpath(__file__))
        self.chrome_driver = os.path.join(self.current, 'chromedriver')
        self.gecko_driver = os.path.join(self.current, 'geckodriver')

    def OpenDriver(self, type='chrome'):
        if type == 'chrome':
            self.driver = wd.Chrome(self.chrome_driver, options=chrome_options) # options=chrome_options
        else:
            self.driver = wd.Firefox() # options=gecko_options
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
        time.sleep(1)

    def web_coordinate(self, url):
        url_parse = urlparse(url)
        query_dict = parse_qs(url_parse.query)

        coordinate_query = query_dict['ms']
        x, y, z = coordinate_query[0].split(',')
        return x, y

    def web_collectURL(self):
        web_dict = {'city_name':[],
                    'district_name':[],
                    'town_name':[],
                    'url':[]}

        city_choice = self.driver.find_element_by_css_selector("span.area:nth-child(2)")
        city_choice.click()
        time.sleep(1)

        city_list = self.driver.find_elements_by_css_selector("li.area_item")
        for idx, city_name in enumerate(city_list):
            if city_name.text == '서울시':
                tmp_city_name = city_name.text
                city_list[idx].click()
                time.sleep(1)
                break

        district_initial = self.driver.find_elements_by_css_selector("li.area_item")
        district_pos = 0
        for i in range(0, len(district_initial)):
            district_list = self.driver.find_elements_by_css_selector("li.area_item")
            district = district_list[district_pos]
            tmp_district_name = district.text

            logger.debug('District name: ' + tmp_district_name)

            district.click()
            time.sleep(1)

            town_initial = self.driver.find_elements_by_css_selector("li.area_item")
            town_pos = 0
            time.sleep(1)
            for j in range(0, len(town_initial)):
                town_list = self.driver.find_elements_by_css_selector("li.area_item")
                town = town_list[town_pos]
                tmp_town_name = town.text

                logger.debug('Town name: ' + tmp_town_name)

                town.click()
                time.sleep(1)

                # At this point, you will get a list of apartments
                apartments_initial = self.driver.find_elements_by_css_selector("li.complex_item")
                time.sleep(1)
                apartment_pos = 0
                for k in range(0, len(apartments_initial)):
                    logger.debug('k iteration: ' + str(k))

                    apartments_list = self.driver.find_elements_by_css_selector("li.complex_item")
                    time.sleep(1)

                    logger.debug('Apartment length at iteration ' + str(k) + ': ' + str(len(apartments_list)))
                    print('apartment list:', len(apartments_list))
                    apartment = apartments_list[apartment_pos]
                    apartment.click()
                    time.sleep(1)

                    apartment_url = self.driver.current_url
                    if apartment_url not in web_dict['url']:
                        web_dict['city_name'].append(tmp_city_name)
                        web_dict['district_name'].append(tmp_district_name)
                        web_dict['town_name'].append(tmp_town_name)
                        web_dict['url'].append(self.driver.current_url)

                    close_list = self.driver.find_element_by_css_selector("button.btn_close:nth-child(3)")
                    close_list.click()
                    time.sleep(1)

                    # Open province
                    province_temp = self.driver.find_element_by_css_selector("span.area:nth-child(2)")
                    time.sleep(1)
                    province_temp.click()
                    time.sleep(1)

                    # Choose province
                    province_temp_list = self.driver.find_elements_by_css_selector("li.area_item")
                    time.sleep(1)
                    province_temp_list[0].click()
                    time.sleep(1)

                    # Choose district
                    district_temp_list = self.driver.find_elements_by_css_selector("li.area_item")
                    time.sleep(1)
                    district_temp_list[i].click()
                    time.sleep(1)

                    # Choose town
                    town_temp_list = self.driver.find_elements_by_css_selector("li.area_item")
                    time.sleep(1)
                    town_temp_list[j].click()
                    time.sleep(1)

                    apartment_pos += 1

                town_click = self.driver.find_element_by_css_selector("a.area_select_item:nth-child(5)")
                town_click.click()
                time.sleep(1)

                # Saving
                collect_df = pd.DataFrame(web_dict)
                print(collect_df)
                collect_df.to_csv('apartment_url.csv', encoding='euc-kr')

                print('csv checkpoint at: ' + tmp_district_name + ' ' + tmp_town_name)
                logger.debug('>>> csv checkpoint at: ' + tmp_district_name + ' ' + tmp_town_name)

                town_pos += 1

            # Returning back to district list
            district_click = self.driver.find_element_by_css_selector("a.area_select_item:nth-child(3)")
            district_click.click()
            time.sleep(1)

            district_pos += 1

        print('-------------')
        print('Complete!')
        self.driver.close()

    def web_collect(self, url_id):
        apartment_id = url_id

        apartment_information = self._apartment_info()
        school_information = self._school_info()

        combine_dict = {'apartment_id':apartment_id, **apartment_information, **school_information}

        combine_df = pd.DataFrame(combine_dict, index=[0])
        print(combine_df)

        header = False if os.path.isfile('result.csv') else True
        combine_df.to_csv('result.csv', mode='a', header=header)

        area_initial = self._tower_area()
        area_choice = 0

        for i in range(len(area_initial)):
            tower_area = self._tower_area()
            area = tower_area[area_choice]
            area.click()
            time.sleep(1)

            get_price = self._tower_price(temp_id=apartment_id, temp_area=area.text)
            if get_price is False:
                return False

            price_df = pd.DataFrame(get_price)
            header_price = False if os.path.isfile('result_price.csv') else True
            price_df.to_csv('result_price.csv', mode='a', header=header_price)

            logger.debug('>>> Price list for: ' + area.text)
            logger.debug(get_price)

            area_choice += 1

        print('-------------')
        print('Complete!')

    @dc.clean_apartment
    def _apartment_info(self):
        apartment_info = self.driver.find_element_by_css_selector('button.complex_link:nth-child(1)')
        apartment_info.click()
        time.sleep(1)

        apartment_built = self.driver.find_elements_by_css_selector("tbody:nth-child(2) > tr:nth-child(2) > td:nth-child(2)")[0].text
        apartment_builder = self.driver.find_elements_by_css_selector("tbody:nth-child(2) > tr:nth-child(4) > td:nth-child(2)")[0].text
        apartment_floor = self.driver.find_elements_by_css_selector("tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(4)")[0].text
        apartment_address = self.driver.find_element_by_css_selector("p.address:nth-child(1)").text
        apartment_parking = self.driver.find_elements_by_css_selector("tbody:nth-child(2) > tr:nth-child(2) > td:nth-child(4)")[0].text

        logger.debug('Apartment build date: ' + apartment_built)
        logger.debug('Apartment company: ' + apartment_builder)
        logger.debug('Apartment floor: ' + apartment_floor)
        logger.debug('Apartment parking: ' + apartment_parking)
        logger.debug('Apartment address: ' + apartment_address)

        return apartment_built, apartment_builder, apartment_floor, apartment_address, apartment_parking

    @dc.clean_school
    def _school_info(self):
        try:
            school_info = self.driver.find_element_by_css_selector(".tab_area_list > a:nth-child(4)")
            if school_info.text != '학군정보':
                school_info = self.driver.find_element_by_css_selector(".tab_area_list > a:nth-child(3)")
        except:
            try:
                school_info = self.driver.find_element_by_css_selector(".tab_area_list > a:nth-child(3)")
                if school_info.text != '학군정보':
                    raise Exception
            except:
                try:
                    school_info = self.driver.find_element_by_css_selector(".tab_area_list > a:nth-child(2)").text
                    if school_info.text != '학군정보':
                        logger.error('>>> COULD NOT FIND SCHOOL INFORMATION!')
                        return False
                except:
                    return False

        school_info.click()
        time.sleep(1)

        school_name = self.driver.find_element_by_css_selector('.detail_box--school > div:nth-child(1) > h5:nth-child(1)').text
        school_dist = self.driver.find_element_by_css_selector('div.town_box:nth-child(2) > div:nth-child(2)').text
        tmp_school_address = self.driver.find_elements_by_css_selector('table.info_table_wrap:nth-child(3) > tbody:nth-child(2) > tr:nth-child(1) > td:nth-child(2)')
        for x in tmp_school_address:
            if x.text != '':
                school_address = x.text
                break
            else:
                school_address = ''

        tmp_school_students = self.driver.find_elements_by_css_selector('table.info_table_wrap:nth-child(3) > tbody:nth-child(2) > tr:nth-child(6) > td:nth-child(2)')
        for x in tmp_school_students:
            if x.text != '':
                school_students = x.text
                break
            else:
                school_students = ''

        logger.debug('School info: ' + school_name)
        logger.debug('School dist: ' + school_dist)
        logger.debug('School address: ' + school_address)
        logger.debug('School students: ' + school_students)

        return school_name, school_dist, school_address, school_students

    @dc.clean_price
    def _tower_price(self, temp_id, temp_area):
        check_buy = self.driver.find_element_by_css_selector('#marketPriceTab1')

        if check_buy.text != '매매':
            return False
        try:
            see_more = self.driver.find_element_by_css_selector("div.detail_price_data:nth-child(4) > button:nth-child(2)")
            while see_more:
                see_more.click()
                time.sleep(1)
        except:
            pass

        rows = self.driver.find_elements_by_css_selector("table.type_real > tbody > tr")

        if not rows:
            return False

        list_period = []
        list_amount = []
        for row in rows:
            txt = row.text.replace('\n', ' ')
            list_period.append(txt[:7])
            list_amount.append(txt[9:])

        return list_period, list_amount, temp_id, temp_area

    def _tower_area(self):
        price = self.driver.find_element_by_css_selector('.tab_area_list > a:nth-child(2)')
        price.click()
        time.sleep(1)

        try:
            dropdown_status = self.driver.find_element_by_css_selector('div.detail_sorting_tabs:nth-child(1) > div:nth-child(1) > div:nth-child(2) > button:nth-child(1)')
            dropdown_status.click()
            time.sleep(1)
        except:
            pass

        area_list = self.driver.find_elements_by_css_selector("#area_tab_list > a")

        return area_list