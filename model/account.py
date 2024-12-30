from db.connection import Connection

class Account:
    def __init__(self):
        self.connection = Connection()

    def get_accounts(self, client):
        connection = self.connection
        if client == 'False':
            sql = "SELECT * FROM `account` WHERE `status`=1"
            accounts = connection.query(sql).fetchall()
        else:
            sql = "SELECT * FROM `account` WHERE `status`=1  and `client`=%s"
            accounts = connection.query(sql, (client)).fetchall()
        return accounts
    
    def get_inactive_accounts(self, client):
        connection = self.connection
        if client == 'False':
            sql = "SELECT * FROM `account` WHERE `status`=2"
            accounts = connection.query(sql).fetchall()
        else:
            sql = "SELECT * FROM `account` WHERE `status`=2  and `client`=%s"
            accounts = connection.query(sql, (client)).fetchall()
        return accounts

    def disable_account(self, account):
        connection = self.connection
        sql = "UPDATE `account` SET `status`=2, `updated_at`=%s WHERE `phone`=%s"
        connection.query(sql, (self.time.get_current_time(), account))
    
    def deleted_account(self, account):
        connection = self.connection
        sql = "UPDATE `account` SET `status`=3, `updated_at`=%s WHERE `phone`=%s"
        connection.query(sql, (self.time.get_current_time(), account))

    def get_seller_accounts(self, client):
        connection = self.connection
        sql = "SELECT * FROM `sl_account`  where status = 1 and `client`=%s"
        accounts = connection.query(sql, (client)).fetchall()
        return accounts

