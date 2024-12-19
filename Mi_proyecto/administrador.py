from Usuario import Usuario
from ReconocimientoFacial import ReconocimientoFacial
import bcrypt

class Administrador:
    def __init__(self, db):
        self.db = db

    def registrar_usuario(self, nombre, correo, contrasena, datos_facial=None):
        # Crear el usuario (hash de la contraseña y datos faciales)
        contrasena_hash = bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt())
        datos_facial_bytes = ReconocimientoFacial.convertir_a_bytes(datos_facial)
        consulta = """
        INSERT INTO usuarios (nombre, correo, contrasena, datos_facial)
        VALUES (%s, %s, %s, %s)
        """
        self.db.ejecutar_consulta(consulta, (nombre, correo, contrasena_hash, datos_facial_bytes))

    def ver_usuarios(self):
        consulta = "SELECT id, nombre, correo FROM usuarios"
        return self.db.obtener_resultados(consulta)

    def eliminar_usuario(self, usuario_id):
        consulta = "DELETE FROM usuarios WHERE id = %s"
        self.db.ejecutar_consulta(consulta, (usuario_id,))
