import json
import sys
import time
import re
import random
import os

sys.path.append('../../')
from model.config import Config
from model.log import Log
from model.target import Target
from model.cookie import Cookie
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import datetime as dt
import random


class ShopeeSeller:
    def __init__(self, driver, seller, client):
        self.config = Config()
        self.log = Log()
        self.driver = driver
        self.seller = seller
        self.target = Target()
        self.client = client
        self.cookie = Cookie()

    def execute(self):
        driver = self.driver
        try:
            seller = self.seller
            account = seller[1]
            all_products = self.target.get_seller_targets(self.client)
            products = random.sample(all_products, 5)
            self.auto_up_product(driver, products, account)
            # size = driver.get_window_size()
            # print("Window size: width = {}px, height = {}px".format(size["width"], size["height"]))
            if  self.login(driver, seller) == False:
                print('Login failed!')
                driver.close()
                return False
            
        except:
            self.log.trace()
        driver.close()

    def auto_remind_5_mins(self, driver):
        try:
            chat = driver.find_element(By.XPATH, '//button[contains(@class, "F5W_lC")]')
            chat.click()
            time.sleep(2)
            mini = driver.find_element(By.XPATH,
                                        '//i[contains(@class, "src-components-MainLayout-index__minimize--30m1T")]')
            mini.click()
            time.sleep(1)
        except:
            self.log.trace()
    
    def auto_up_product(self, driver, products, account):
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//input[@class="shopee-input__input"]'))
            )
            try:
                button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.XPATH,
                        "//button[contains(@class,'next-button')]"))
                )
                button.click()
            except:
                pass
            try:
                button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.XPATH,
                        "//div[contains(@class,'guide-modal')]//button[contains(@class,'shopee-button--primary')]"))
                )
                button.click()
            except:
                pass
            try:
                button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.XPATH,
                        "//button[contains(@class,'guideBtn')]"))
                )
                button.click()
            except:
                pass
            search_input = driver.find_element(By.XPATH,'//input[@class="shopee-input__input"]')
            for product in products:
                search_input.send_keys(product[1])
                search_input.send_keys(Keys.ENTER)
                time.sleep(10)                
                driver.execute_script("window.scrollTo(0,500)")                
                try:
                    WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.XPATH,
                        "//div[@class='list-view-action']//button[contains(@class,'shopee-button--link')]"))
                )
                    driver.execute_script("window.scrollTo(0,800)")
                    action_link = driver.find_element(By.XPATH,
                        "//div[@class='list-view-action']//div[contains(@class,'shopee-dropdown')]//button[contains(@class,'shopee-button--link')]")
                    action_link.click()
                    time.sleep(3)
                    up_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable(
                            (By.XPATH,
                            "//div[contains(@class, 'more-dropdown-menu') and contains(@style, 'absolute')]//span[contains(text(), 'Đẩy sản phẩm')]"))
                    )
                    ActionChains(driver).move_to_element(up_button).click().perform()
                    #up_button.click()
                    time.sleep(3)
                    toast_error = driver.find_elements(By.XPATH,
                        '//i[contains(@class, "shopee-toast__icon--error")]')
                    print("Total error: " + str(len(toast_error)))
                    if len(toast_error) == 0:
                        sku = driver.find_element(By.XPATH,
                            "//div[@class='product-sku']").text
                        self.log.save_log(sku, product[1], 'shopee-up', account, self.client, {})
                        time.sleep(5)
                except:
                    self.log.trace()
                search_input.send_keys(Keys.CONTROL + "a")
                search_input.send_keys(Keys.DELETE)
        except:
            self.log.trace()

    def login(self, driver, account):
        name =  account[1]
        cookie = account[5]
        driver.get("https://banhang.shopee.vn/portal/product/list/all")
        time.sleep(2)
        driver = self.cookie.load_cookie(driver, cookie)
        print("Loading cookie for %s ..." % (name))
        time.sleep(2)
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//span[contains(@class, "account-name")]'))
            )                     
            print('Already Logged! ')
            time.sleep(2)
            driver.refresh()   
            return True
        except:
            self.log.trace()
            print('Can not login!')
        