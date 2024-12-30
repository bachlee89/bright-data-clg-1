import pymysql.cursors
from model.config import Config


class Connection:
    def __init__(self):
        self.config = Config()

    def init_db(self):
        db_config = self.get_db_config()
        db = pymysql.connect(host=db_config['host'], user=db_config['usename'], password=db_config['password'],
                             db=db_config['dbname'])
        return db

    def get_db_config(self):
        return self.config.get_section_config('Mysql')

    def query(self, sql, args=None):
        connection = self.init_db()
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, args)
                result = cursor
                connection.commit()
                return result

        except pymysql.InternalError as error:
            code, message = error.args
            print(message)
        finally:
            connection.close()

    def select(self, sql, args=None):
        connection = self.init_db()
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, args)
                result = cursor.fetchone()
        finally:
            connection.close()
        return result

    def select_all(self, sql, args=None):
        connection = self.init_db()
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, args)
                result = cursor.fetchall()
        finally:
            connection.close()
        return result
