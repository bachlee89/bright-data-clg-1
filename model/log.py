from .config import Config
from .time import Time
from datetime import datetime
import requests
from db.connection import Connection
import os
import sys
import time


class Log:
    def __init__(self):
        self.path = Config().get_base_dir('var') + 'log/'
        self.time = Time()
        self.connection = Connection()

    def log(self, message, type="message"):
        current_time = "[" + self.time.get_current_time() + "]"
        client_config = Config().get_section_config('Client')
        if type == 'debug' and client_config['debug'] != 'True':
            return 0
        with open(self.path + 'system.log', 'a', encoding='utf-8') as f:
            message = current_time + "[" + type + "]: " + message
            f.write(message + '\n')
            return 1

    def save_log(self, target, key, type, account, client, proxy={}):
        sql = "INSERT INTO `log` (`target`, `key`,`type`,`account`,`client`, `created_at`, `ip`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        self.connection.query(sql,
                              (target, key, type, str(account), client, self.time.get_current_time(),
                               self.get_ip(proxy)))

    def get_ip(self, proxy={}):
        if len(proxy) > 0:
            proxies = {
                "http": "http://" + proxy['ip'] + ":" + proxy['port'],
                "https": "http://" + proxy['ip'] + ":" + proxy['port']
                }
            ip = requests.get('https://checkip.amazonaws.com', proxies=proxies).text.strip()
            return ip
        ip = requests.get('https://checkip.amazonaws.com').text.strip()
        return ip

    def verify(self, client):
        failed = 0
        while 1:
            if failed > 4:
                return False
            try:
                sql = "SELECT * FROM `log` WHERE client LIKE %s ORDER BY id DESC LIMIT 1"
                log = self.connection.select(sql, client)
                f = "%Y-%m-%d %H:%M:%S"
                current_time = datetime.strptime(self.time.get_current_time(), f)
                created_at = log[7]
                time_diff = current_time - created_at
                total_seconds = time_diff.total_seconds()
                if total_seconds > 3600:
                    return False
                return True
            except:
                self.trace()
                failed += 1
                disconnect = 'rasdial /disconnect'
                connect = 'rasdial 3531'
                os.system(disconnect)
                time.sleep(5)
                os.system(connect)
                print("Resetting Dcom ....")
                time.sleep(10)
                continue

    def verify_cart(self, client):
        try:
            sql = "SELECT account FROM `log` WHERE `account` like %s AND `type` LIKE %s AND DATE(created_at)=DATE(NOW())"
            accounts = self.connection.select(sql, (client, '%remove%'))
            if accounts is None:
                return True
            return False
        except:
            pass
        return False

    def trace(self):
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        self.log(str(sys.exc_info()), 'debug')
        self.log(str(exc_type) + '-' + fname + '-' + str(exc_tb.tb_lineno), 'error')
