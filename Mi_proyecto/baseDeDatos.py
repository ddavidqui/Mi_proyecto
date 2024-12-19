import mysql.connector

class BaseDeDatos:
    def __init__(self, host, user, password, database):

        self.connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='2024',
            database='gymapp'
        )
        self.cursor = self.connection.cursor()

        

    def ejecutar_consulta(self, consulta, datos=None):
        self.cursor.execute(consulta, datos or ())
        self.connection.commit()
        return self.cursor

    def obtener_resultados(self, consulta, datos=None):
        self.cursor.execute(consulta, datos or ())
        return self.cursor.fetchall()

    def cerrar_conexion(self):
        self.cursor.close()
        self.connection.close()
