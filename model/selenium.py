from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import os
from .config import Config
from .log import Log

class Selenium:
    def __init__(self, auth):
        self.auth = auth
        self.config = Config()
        self.log = Log()

    def get_bright_chrome_driver(self, name, headless=True):
        options = ChromeOptions()
        if headless == True:
            options.headless = headless
            options.add_argument('--headless')
            options.add_argument('--window-size=1920,1080')
        options.add_argument("user-data-dir=" + self.get_profile_path(name))
        print('Connecting to Scraping Browser...')
        SBR_WEBDRIVER = f'https://{self.auth}@brd.superproxy.io:9515'
        sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
        try:
            driver = Remote(command_executor=sbr_connection, options=options)
            return driver
        except:
            self.log.log()
            return False
    
    def get_profile_path(self, name):
        path = self.config.get_base_dir('tmp') + "/anti-detect/profile/" + name.strip()
        if os.path.isdir(path) == True:
            return path
        os.makedirs(path)
        return path
    
    
