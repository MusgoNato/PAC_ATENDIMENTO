import pymysql
class ServicoBancoDeDados():
    __params = None

    def __init__(self, host, user, password, database="riobrilhantems_dev_pac"):
        self.conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            cursorclass=pymysql.cursors.DictCursor
        )
        self.cursor = self.conn.cursor()

    @classmethod
    def setParametros(cls, host, user, password, database="riobrilhantems_dev_pac"):
        cls.__params = (host, user, password, database)