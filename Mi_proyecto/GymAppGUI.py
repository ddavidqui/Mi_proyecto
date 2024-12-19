import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime
from ReconocimientoFacial import ReconocimientoFacial
from baseDeDatos import BaseDeDatos
from Usuario import Usuario
from administrador import Administrador

class GymAppGUI:
    def __init__(self, db):
        self.db = db
        self.root = tk.Tk()
        self.root.title("GymApp - Gestión de Usuarios")
        self.root.geometry("400x300")

        self.nombre_var = tk.StringVar()
        self.correo_var = tk.StringVar()
        self.contrasena_var = tk.StringVar()

        self.admin_correo_var = tk.StringVar()
        self.admin_contrasena_var = tk.StringVar()

        self.datos_facial = None

        self.admin = Administrador(db)

        self.crear_menu_principal()

    def limpiar_campos(self):
        """Limpia todos los campos de entrada de texto y datos faciales."""
        self.nombre_var.set('')
        self.correo_var.set('')
        self.contrasena_var.set('')
        self.admin_correo_var.set('')
        self.admin_contrasena_var.set('')
        self.datos_facial = None

    def crear_menu_principal(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # Limpia los campos cuando se vuelve al menú principal
        self.limpiar_campos()

        tk.Label(self.root, text="GymApp", font=("Arial", 18)).pack(pady=10)
        tk.Button(self.root, text="Iniciar Sesión Usuario", command=self.abrir_inicio_sesion, width=30).pack(pady=10)
        tk.Button(self.root, text="Iniciar Sesión como Administrador", command=self.abrir_inicio_sesion_admin, width=30).pack(pady=10)
        tk.Button(self.root, text="Salir", command=self.root.quit, width=30).pack(pady=10)

    def abrir_inicio_sesion(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # Limpia campos al abrir la ventana de inicio de sesión
        self.limpiar_campos()

        tk.Label(self.root, text="Inicio de Sesión (Usuario)", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.root, text="Correo:").pack()
        tk.Entry(self.root, textvariable=self.correo_var).pack()

        tk.Label(self.root, text="Contraseña:").pack()
        tk.Entry(self.root, textvariable=self.contrasena_var, show="*").pack()

        tk.Button(self.root, text="Iniciar Sesión (Contraseña)", command=self.iniciar_sesion_contrasena).pack(pady=5)
        tk.Button(self.root, text="Iniciar Sesión (Reconocimiento Facial)", command=self.iniciar_sesion_facial).pack(pady=5)
        tk.Button(self.root, text="Volver", command=self.crear_menu_principal).pack(pady=5)

    def abrir_inicio_sesion_admin(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # Limpia campos al abrir el inicio de sesión de administrador
        self.limpiar_campos()

        tk.Label(self.root, text="Inicio de Sesión (Administrador)", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.root, text="Usuario:").pack()
        tk.Entry(self.root, textvariable=self.admin_correo_var).pack()

        tk.Label(self.root, text="Contraseña:").pack()
        tk.Entry(self.root, textvariable=self.admin_contrasena_var, show="*").pack()

        tk.Button(self.root, text="Iniciar Sesión Admin", command=self.iniciar_sesion_admin).pack(pady=5)
        tk.Button(self.root, text="Volver", command=self.crear_menu_principal).pack(pady=5)

    def iniciar_sesion_admin(self):
        correo = self.admin_correo_var.get()
        contrasena = self.admin_contrasena_var.get()

        # Autenticación del administrador
        if correo == "admin" and contrasena == "2024":
            messagebox.showinfo("Éxito", "Inicio de sesión como administrador exitoso.")
            self.mostrar_panel_administrador()
        else:
            messagebox.showwarning("Error", "Credenciales de administrador incorrectas.")

    def iniciar_sesion_contrasena(self):
        correo = self.correo_var.get()
        contrasena = self.contrasena_var.get()

        usuario_id = Usuario.autenticar(self.db, correo, contrasena)
        if usuario_id:
            self.registrar_ingreso(usuario_id)
            messagebox.showinfo("Éxito", "Bienvenido al GYM UNAL SEDE LA PAZ adelante...")
            self.crear_menu_principal()
        else:
            messagebox.showwarning("Error", "Credenciales incorrectas.")

    def iniciar_sesion_facial(self):
        messagebox.showinfo("Captura", "Por favor, mira a la cámara y presiona 'q' para capturar.")
        datos_facial_actual = ReconocimientoFacial.capturar_datos_facial()

        if datos_facial_actual is None:
            messagebox.showwarning("Error", "No se pudo capturar el rostro actual. Intente de nuevo.")
            return

        consulta = "SELECT id, datos_facial FROM usuarios"
        usuarios = self.db.obtener_resultados(consulta)

        for usuario_id, datos_facial_registrados in usuarios:
            datos_facial_registrados_array = ReconocimientoFacial.convertir_a_ndarray(datos_facial_registrados)
            if ReconocimientoFacial.comparar_rostros(datos_facial_registrados_array, datos_facial_actual):
                self.registrar_ingreso(usuario_id)
                messagebox.showinfo("Éxito", "Bienvenido al GYM UNAL SEDE LA PAZ adelante...")
                self.crear_menu_principal()
                return

        messagebox.showwarning("Error", "No se encontró coincidencia facial.")

    def registrar_ingreso(self, usuario_id):
        consulta = "INSERT INTO registros_ingresos (usuario_id) VALUES (%s)"
        self.db.ejecutar_consulta(consulta, (usuario_id,))
        print(f"Ingreso registrado: {datetime.now()}")

    def mostrar_panel_administrador(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # Limpia campos al mostrar el panel de administrador
        self.limpiar_campos()

        tk.Label(self.root, text="Panel de Administración", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.root, text="Ver Usuarios", command=self.ver_usuarios).pack(pady=5)
        tk.Button(self.root, text="Registrar Usuario", command=self.abrir_registro_usuario_admin).pack(pady=5)
        tk.Button(self.root, text="Eliminar Usuario", command=self.abrir_ventana_eliminar_usuario).pack(pady=5)
        tk.Button(self.root, text="Volver", command=self.crear_menu_principal).pack(pady=5)

    def ver_usuarios(self):
        usuarios = self.admin.ver_usuarios()
        if usuarios:
            info = "ID | NOMBRE | CORREO\n"
            info += "\n".join([f"{u[0]} | {u[1]} | {u[2]}" for u in usuarios])
        else:
            info = "No hay usuarios registrados."
        messagebox.showinfo("Lista de Usuarios", info)

    def abrir_registro_usuario_admin(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # Limpia campos al abrir el registro de usuario admin
        self.limpiar_campos()

        tk.Label(self.root, text="Registro de Usuario (Admin)", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.root, text="Nombre:").pack()
        tk.Entry(self.root, textvariable=self.nombre_var).pack()

        tk.Label(self.root, text="Correo:").pack()
        tk.Entry(self.root, textvariable=self.correo_var).pack()

        tk.Label(self.root, text="Contraseña:").pack()
        tk.Entry(self.root, textvariable=self.contrasena_var, show="*").pack()

        tk.Button(self.root, text="Capturar Datos Faciales", command=self.capturar_datos_facial).pack(pady=5)
        tk.Button(self.root, text="Registrar", command=self.registrar_usuario_admin).pack(pady=5)
        tk.Button(self.root, text="Volver", command=self.mostrar_panel_administrador).pack(pady=5)

    def registrar_usuario_admin(self):
        nombre = self.nombre_var.get()
        correo = self.correo_var.get()
        contrasena = self.contrasena_var.get()

        if not (nombre and correo and contrasena):
            messagebox.showwarning("Error", "Todos los campos son obligatorios.")
            return

        self.admin.registrar_usuario(nombre, correo, contrasena, self.datos_facial)
        messagebox.showinfo("Éxito", "Usuario registrado exitosamente.")

        # Limpia campos luego del registro
        self.limpiar_campos()
        self.mostrar_panel_administrador()

    def abrir_ventana_eliminar_usuario(self):
        # Crea una nueva ventana para mostrar usuarios y eliminarlos
        ventana_eliminar = tk.Toplevel(self.root)
        ventana_eliminar.title("Eliminar Usuario")
        ventana_eliminar.geometry("300x300")

        tk.Label(ventana_eliminar, text="Selecciona un usuario para eliminar", font=("Arial", 14)).pack(pady=10)

        # Listbox para mostrar usuarios
        lista_usuarios = tk.Listbox(ventana_eliminar, width=40)
        lista_usuarios.pack(pady=10)

        usuarios = self.admin.ver_usuarios()
        # Cargamos la lista con ID, Nombre, Correo
        for u in usuarios:
            lista_usuarios.insert(tk.END, f"{u[0]} - {u[1]} - {u[2]}")

        def eliminar_usuario_seleccionado():
            seleccion = lista_usuarios.curselection()
            if seleccion:
                seleccionado = lista_usuarios.get(seleccion)
                # seleccionado tiene formato "id - nombre - correo"
                usuario_id_str = seleccionado.split(" - ")[0]
                usuario_id = int(usuario_id_str)
                self.admin.eliminar_usuario(usuario_id)
                messagebox.showinfo("Éxito", "Usuario eliminado exitosamente.")
                ventana_eliminar.destroy()
                self.mostrar_panel_administrador()
            else:
                messagebox.showwarning("Advertencia", "Debes seleccionar un usuario para eliminar.")

        tk.Button(ventana_eliminar, text="Eliminar Usuario Seleccionado", command=eliminar_usuario_seleccionado).pack(pady=5)
        tk.Button(ventana_eliminar, text="Cerrar", command=ventana_eliminar.destroy).pack(pady=5)

    def capturar_datos_facial(self):
        self.datos_facial = ReconocimientoFacial.capturar_datos_facial()
        if self.datos_facial is not None:
            messagebox.showinfo("Éxito", "Datos faciales capturados exitosamente.")
        else:
            messagebox.showwarning("Error", "No se pudo capturar datos faciales correctamente.")

    def ejecutar(self):
        self.root.mainloop()

if __name__ == "__main__":
    db = BaseDeDatos(host="localhost", user="root", password="2024", database="gymapp")
    app = GymAppGUI(db)
    app.ejecutar()
