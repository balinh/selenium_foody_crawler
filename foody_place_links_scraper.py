from selenium import webdriver
from foody_login_task import login

filename = 'link/foody_place_links'
loop = 300
place_url = 'https://foody.vn/'


class FoodyPlaceLinkScrapper:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.is_logged_in = False

    def scrap(self, region):
        self.driver.get(place_url + region)
        if not self.is_logged_in:
            self.is_logged_in = login(self)
        for i in range(1, loop):
            self.click_load_more(i)
            self.scrap_links(region)

    def click_load_more(self, i):
        load_more_btn = self.driver.find_element_by_css_selector('a.fd-btn-more')
        self.driver.execute_script("arguments[0].click();", load_more_btn)
        print('Clicked Load more Button ' + str(i) + ' times')

    def scrap_links(self, region):
        place_links = self.driver.find_elements_by_css_selector(
            'div.content-container div.content-item div.items-content div.title a')
        out = open(filename + '_' + region + '_v2.txt', 'a')
        for link in place_links:
            print(link.get_attribute('href'))
            out.write(link.get_attribute('href') + '\n')
            self.driver.execute_script("arguments[0].parentNode.removeChild(arguments[0]);", link)
        out.close()
        print("Retrieved " + str(len(place_links)) + " links")

    def remove_item(self):
        return True


place_link_scrapper = FoodyPlaceLinkScrapper()
place_link_scrapper.scrap('ho-chi-minh')
place_link_scrapper.scrap('ha-noi')
