import bcrypt
from ReconocimientoFacial import ReconocimientoFacial

class Usuario:
    def __init__(self, nombre, correo, contrasena, datos_facial=None):
        self.nombre = nombre
        self.correo = correo
        self.contrasena = bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt())
        self.datos_facial = ReconocimientoFacial.convertir_a_bytes(datos_facial)

    @staticmethod
    def obtener_datos_facial(db, usuario_id):
        consulta = "SELECT datos_facial FROM usuarios WHERE id = %s"
        resultados = db.obtener_resultados(consulta, (usuario_id,))
        if resultados:
            datos_facial_bytes = resultados[0][0]
            return ReconocimientoFacial.convertir_a_ndarray(datos_facial_bytes)
        return None

    @staticmethod
    def autenticar(db, correo, contrasena):
        consulta = "SELECT id, contrasena FROM usuarios WHERE correo = %s"
        resultado = db.obtener_resultados(consulta, (correo,))
        if resultado:
            usuario_id, contrasena_hash = resultado[0]
            if isinstance(contrasena_hash, str):
                contrasena_hash = contrasena_hash.encode('utf-8')
            if bcrypt.checkpw(contrasena.encode('utf-8'), contrasena_hash):
                return usuario_id
        return None
