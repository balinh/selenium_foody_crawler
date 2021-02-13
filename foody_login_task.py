from selenium.webdriver.common.keys import Keys


def login(self):
    try:
        print("Login")
        # Click Item Kham pha
        discovery_item = self.driver.find_element_by_css_selector('a[onclick="#places"]')
        discovery_item.click()
    except Exception:
        print("This page has no Intro popup")
    # Click nut Dang nhap
    login_btn = self.driver.find_element_by_xpath('//*[@id="accountmanager"]/a/span')
    self.driver.execute_script("arguments[0].click();", login_btn)
    self.driver.implicitly_wait(5)

    # Nhap Email
    email = self.driver.find_element_by_xpath('//input[@ng-model="Data.Email"]')
    email.send_keys('eteem.axic@gmail.com')

    # Nhap password
    password = self.driver.find_element_by_xpath('//input[@ng-model="Data.Password"]')
    password.send_keys('ilovemeete')
    password.send_keys(Keys.RETURN)

    # Click nut Dang nhap tren popup
    # login_popup_btn = self.driver.find_element_by_css_selector('a.btn-login')
    # self.driver.execute_script("arguments[0].click();", login_popup_btn)
    return True
