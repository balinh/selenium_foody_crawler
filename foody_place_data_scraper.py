import csv
import logging
import random
from selenium import webdriver
from selenium.webdriver.common.proxy import *
from foody_login_task import login
from multiprocessing import Pool

link_file = 'link/foody_place_links'
data_file = 'data/foody_place_data'


class PlaceData:
    def __init__(self):
        self.name = None
        self.phone = []
        self.url = None
        self.review_count = None
        self.category = None
        self.district = None
        self.city = None


class FoodyMerchantDataScrapper:
    def __init__(self, filename):
        self.driver = webdriver.Firefox(proxy=get_proxy())
        self.filename = filename
        self.is_logged_in = False
        self.csv_file = None
        self.region = None

    def scrap(self, region):
        try:
            self.region = region
            while len(link_stack):
                self.scrap_single_url(link_stack.pop())
        except Exception as e:
            logging.error("Exception at scrap function", e)

    def scrap_single_url(self, url):
        print('Scrap URL ' + url)
        self.driver.get(url)

        # if not self.is_logged_in:
        login(self)
        self.click_show_phone_button()

        place_data = self.extract_place_data()
        place_data.url = url
        if place_data:
            self.save_place_data(place_data)
        self.driver.close()

    def save_place_data(self, place_data):
        print("Save data")
        region = str(place_data.url).split('/')[3]
        self.csv_file = open(data_file + '_' + region + '.csv', 'a', newline='')
        place_data_arr = [place_data.name,
                          ', '.join(place_data.phone),
                          place_data.review_count,
                          place_data.url,
                          place_data.category,
                          place_data.district,
                          place_data.city
                          ]
        place = csv.writer(self.csv_file, delimiter='|',
                           quotechar='|', quoting=csv.QUOTE_MINIMAL)
        print('|'.join(place_data_arr))
        place.writerow(place_data_arr)
        self.csv_file.close()

    def extract_place_data(self):
        print("Extract data")
        place_data = PlaceData()
        try:
            res_common_info = self.driver.find_element_by_css_selector('div.res-common-info > div.main-info-title')
            category_container = res_common_info.find_element_by_css_selector('div.category')
            address_info = self.driver.find_element_by_css_selector('div.res-common-add')

            name = res_common_info.find_element_by_css_selector('h1')
            phone_parents = self.driver.find_elements_by_css_selector(
                'div.microsite-popup-phone-number table tbody tr td:nth-child(even)')
            review_count = self.driver.find_element_by_css_selector(
                'div#res-summary-point > div.microsite-points-summary > div.microsite-top-points-block > div.microsite-review-count')
            category = category_container.find_element_by_css_selector('div.category-items > a')
            district = address_info.find_element_by_css_selector('span:nth-child(4) > a > span')
            city = address_info.find_element_by_css_selector('span:nth-child(5)')
            # Gan du lieu vao doi tuong
            place_data.name = str(name.text)
            place_data.review_count = str(review_count.text)
            place_data.category = str(category.text)
            place_data.district = str(district.text)
            place_data.city = str(city.text)
            for p in phone_parents:
                place_data.phone.append(str(p.text).replace(' ', ''))
        except Exception as e:
            logging.error(str(e))
            place_data = None
        finally:
            return place_data

    def click_show_phone_button(self):
        print("Click show phone button")
        show_phone_btn = self.driver.find_element_by_css_selector('#show-phone-number')
        self.driver.execute_script("arguments[0].click();", show_phone_btn)


def get_links(filename, region):
    out = open(filename + '_' + region + '.txt')
    raw_content = out.readlines()
    links = [x.strip() for x in raw_content]
    out.close()
    return links


def get_proxy():
    my_proxy = proxy_stack[random.randint(0, len(proxy_stack) - 1)]

    proxy = Proxy({
        'proxyType': ProxyType.MANUAL,
        'httpProxy': my_proxy,
        'ftpProxy': my_proxy,
        'sslProxy': my_proxy,
        'noProxy': ''  # set this value as desired
    })

    return proxy


def run_scrapper(url):
    place_link_scrapper = FoodyMerchantDataScrapper(None)
    place_link_scrapper.scrap_single_url(url)
    # place_link_scrapper.scrap('backup')
    # place_link_scrapper.scrap('ho-chi-minh')
    # place_link_scrapper.scrap('ha-noi')


link_stack = get_links(link_file, 'backup')
proxy_stack = [
    '123.30.238.16:3128',
    '115.84.179.131:80',
    '137.59.44.47:80',
    '103.28.36.56:8888',
    '119.15.169.125:3128',
    '119.15.169.114:3128',
    '103.205.107.81:8080',
    '137.59.44.47:8080',
]

# TODO: Use proxy
print("Start scrapping")
# run_scrapper(link_stack)
pool = Pool(5)
pool.map(run_scrapper, link_stack)
pool.join()
pool.close()
print("Finished Scrapping")
