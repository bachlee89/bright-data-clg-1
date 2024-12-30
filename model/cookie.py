from db.connection import Connection
from .time import Time
import json

class Cookie:
    def __init__(self):
        self.connection = Connection()
        self.time = Time()

    def get_cookie(self, account):
        connection = self.connection
        sql = "SELECT * FROM `cookie` where `account`=%s"
        cookie = connection.select(sql, (account))
        return cookie

    def create_cookie(self, account, value, client):
        sql = "INSERT INTO `cookie` (`account`,`value`, `client`) VALUES (%s, %s, %s)"
        self.connection.query(sql, (account, json.dumps(value), client))

    def update_cookie(self, account, value, client):
        sql = "UPDATE `cookie` SET `value`=%s,`client`=%s, `updated_at`=%s WHERE `account`=%s"
        self.connection.query(sql, (json.dumps(value), client, self.time.get_current_time(), account))

    def delete_cookie(self, account):
        sql = "DELETE FROM `cookie` WHERE `account`=%s"
        self.connection.query(sql, (account))
    
    def load_cookie(self, driver, value):
        cookies = json.loads(value)
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.refresh()
        return driver
