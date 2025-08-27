import pymysql

class ServicoBancoDeDados():
    """Classe referente ao servico do banco de dados"""
    
    __instancia = None
    
    def __init__(self, host, user, password, database="riobrilhantems_dev_pac"):
        """Construtor do servico de banco de dados ad aplicacao"""
        self.conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
        database=database,
        cursorclass=pymysql.cursors.DictCursor
        )
        self.cursor = self.conn.cursor()

    @classmethod
    def getInstancia(cls):
        """Retorno da instancia do servico do banco de dados"""
        if cls.__instancia is None:
            cls.__instancia = ServicoBancoDeDados()
        return cls.__instancia
    
    
    def getAll_infoDB(self, query, params=None):
        """Execucao SELECT para retorno de todos os resultados do banco de dados"""
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
    

    def encerraConexaoBD(self):
        """Encerra a conexao com o servico de banco de dados"""
        self.cursor.close()
        self.conn.close()