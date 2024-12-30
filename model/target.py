from db.connection import Connection


class Target:
    def __init__(self):
        self.connection = Connection()

    def get_targets_by_key(self, key):
        connection = self.connection
        sql = "SELECT * FROM `target` where %s LIKE CONCAT(%s, `keyword`, %s) and `status`=1"
        targets = connection.query(sql, (key, '%', '%')).fetchall()
        return targets

    def get_all_boss(self):
        connection = self.connection
        sql = "SELECT * FROM `target` where `type`='boss' and `status`=1"
        targets = connection.query(sql).fetchall()
        return targets

    def get_all_shop(self):
        connection = self.connection
        sql = "SELECT * FROM `target` where `type`='shop' and `status`=1"
        targets = connection.query(sql).fetchall()
        return targets

    def total_click(self, link, day=0):
        connection = self.connection
        sql = "SELECT * FROM `log` WHERE `target` LIKE %s AND DATE(created_at)=DATE(SUBDATE(NOW(), %s))"
        targets = connection.query(sql, ("%" + link + "%", day)).fetchall()
        return len(targets)

    def total_click_by_account(self, link, account, day=0):
        connection = self.connection
        sql = "SELECT * FROM `log` WHERE `target` LIKE %s AND `account`=%s AND DATE(created_at)>DATE(SUBDATE(NOW(), %s))"
        targets = connection.query(sql, ("%" + link + "%", account, day)).fetchall()
        return len(targets)

    def total_add_to_cart_by_account(self, link, account, day=0):
        connection = self.connection
        sql = "SELECT * FROM `log` WHERE `target` LIKE %s AND `account`=%s AND DATE(created_at)>DATE(SUBDATE(NOW(), %s)) AND `type`='shopee-seo-cart'"
        targets = connection.query(sql, ("%" + link + "%", account, day)).fetchall()
        return len(targets)
    
    def total_click_by_account_today(self, link, account, type):
        connection = self.connection
        sql = "SELECT * FROM `log` WHERE `target` LIKE %s AND `account`=%s AND DATE(created_at)=DATE(NOW()) AND `type`=%s"
        targets = connection.query(sql, ("%" + link + "%", account, type)).fetchall()
        return len(targets)

    def get_seller_targets(self, seller):
        connection = self.connection
        sql = "SELECT * FROM `sl_target` where `client`=%s and `status`=1"
        targets = connection.query(sql, (seller)).fetchall()
        return targets
