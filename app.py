#!/usr/bin/env python3

from scraper.shopeeseller import ShopeeSeller
from model.config import Config
from model.log import Log
from model.account import Account
from model.thread.connector import ThreadConnector
from model.selenium import Selenium
import time

def run():    
    client_config = Config().get_section_config('Client')
    client_name = client_config['name']
    bright_auth = client_config['bright_auth']
    headless = False
    if 'driver_headless' in client_config and client_config['driver_headless'] == 'True':
        headless = True
    while 1:
        try:
            sellers = Account().get_seller_accounts(client_name)
            threads = []
            for seller in sellers:
                seller_name = seller[1]
                selenium = Selenium(bright_auth)
                driver = selenium.get_bright_chrome_driver(seller_name, headless)
                if driver == False:
                    print('Can not create Driver...')
                    continue
                shopee_seller = ShopeeSeller(driver, seller, client_name)
                thread = ThreadConnector("Thread-Shopee-Seller: "+ seller[1], shopee_seller, 15)
                thread.start()
                threads.append(thread)
            for t in threads:
                t.join(120)
            time.sleep(600)
        except:
            Log().trace()
        
if __name__ == '__main__':
    run()
