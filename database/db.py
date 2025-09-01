import pymysql
class ServicoBancoDeDados():
    __instancia = None
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

    @classmethod
    def getInstancia(cls):
        if cls.__instancia is None:
            if cls.__params is None:
                raise Exception("Parametros de conexão não foram definidos")
            cls.__instancia = ServicoBancoDeDados(*cls.__params)
        return cls.__instancia
