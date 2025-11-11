import sqlite3
import hashlib
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import ImageTk, Image
from datetime import datetime

# ==============================
# EXCEPCIONES PERSONALIZADAS
# ==============================

class MenorEdadError(Exception):
    """Excepción lanzada si el usuario es menor de edad."""
    pass

class UsuarioBloqueadoError(Exception):
    """Excepción lanzada si el usuario está bloqueado."""
    pass

# ==============================
# GESTIÓN DE BASE DE DATOS
# ==============================

class GestorBD:
    def __init__(self):
        self.conn = sqlite3.connect("users.db")
        self.crear_tabla()

    def crear_tabla(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nickname TEXT UNIQUE,
                        passw TEXT,
                        birthday TEXT,
                        blocked INTEGER
                    )''')
        self.conn.commit()

    def insertar_usuario(self, nickname, passw, birthday, blocked=False):
        try:
            cursor = self.conn.cursor()
            passw_hash = hashlib.md5(passw.encode()).hexdigest()
            cursor.execute("INSERT INTO usuarios (nickname, passw, birthday, blocked) VALUES (?,?,?,?)",
                           (nickname, passw_hash, birthday, int(blocked)))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def validar_usuario(self, nickname, passw):
        cursor = self.conn.cursor()
        passw_hash = hashlib.md5(passw.encode()).hexdigest()
        cursor.execute("SELECT * FROM usuarios WHERE nickname=? AND passw=?", (nickname, passw_hash))
        return cursor.fetchone()

# ==============================
# CLASE PRINCIPAL DE LOGIN
# ==============================

class VentanaLogin:
    def __init__(self, root):
        self.db = GestorBD()
        self.root = root
        self.root.title("Ventana de acceso")
        self.root.geometry("420x400")
        self.root.resizable(0,0)

        # ENCABEZADO
        frame_enc = Frame(root)
        frame_enc.pack()
        img_login = Image.open("login.png")
        img_render = ImageTk.PhotoImage(img_login.resize((30,30)))
        label_img = Label(frame_enc, image=img_render)
        label_img.image = img_render
        label_img.grid(row=0,column=0,padx=10,pady=30)
        Label(frame_enc, text="INICIAR SESIÓN", font=("Comic Sans", 16)).grid(row=0, column=1)

        # FORMULARIO
        frame_form = LabelFrame(root, text="Datos", font=("Comic Sans", 11))
        frame_form.pack(padx=10, pady=10)

        Label(frame_form,text="Usuario:",font=("Comic Sans", 13)).grid(row=0,column=0,padx=10,pady=(20,10))
        self.user = Entry(frame_form,width=25,font=("Comic Sans", 13))
        self.user.grid(row=0,column=1,padx=10,pady=(20,10))

        Label(frame_form,text="Contraseña:",font=("Comic Sans", 13)).grid(row=1,column=0,padx=10,pady=(10,20))
        self.passw = Entry(frame_form,show="*",width=25,font=("Comic Sans", 13))
        self.passw.grid(row=1,column=1,padx=10,pady=(10,20))

        # BOTONES
        frame_btn = Frame(root)
        frame_btn.pack()

        Button(frame_btn,text="Acceder",command=self.loginuser,bg="black",fg="white",
               font=("Comic Sans",13),width=12).grid(row=0,column=0,padx=10,pady=10)

        Button(frame_btn,text="Registrar nuevo usuario",command=self.abrir_registro,
               font=("Comic Sans",11)).grid(row=1,column=0,padx=10,pady=5)

    # ==============================
    # FUNCIONES DE LOGIN
    # ==============================

    def loginuser(self):
        user = self.user.get().strip()
        passw = self.passw.get().strip()

        if not user or not passw:
            messagebox.showwarning("Aviso", "Por favor, completa todos los campos.")
            return

        data = self.db.validar_usuario(user, passw)
        if data:
            try:
                # data: (id, nickname, passw, birthday, blocked)
                self.comprobar_permisos(data)
                self.abrir_programa(data[1])
            except MenorEdadError:
                messagebox.showerror("Acceso denegado", "Eres menor de edad y no puedes acceder.")
            except UsuarioBloqueadoError:
                messagebox.showerror("Acceso denegado", "Tu usuario está bloqueado.")
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

    def comprobar_permisos(self, data):
        _, _, _, birthday, blocked = data
        # Verificar edad
        fecha_nac = datetime.strptime(birthday, "%Y-%m-%d")
        edad = (datetime.now() - fecha_nac).days / 365.25
        if edad < 18:
            raise MenorEdadError
        if blocked == 1:
            raise UsuarioBloqueadoError

    def abrir_programa(self, nickname):
        self.root.destroy()
        new_window = Tk()
        new_window.title("Acceso al programa")
        new_window.geometry("600x400")

        frame_enc = Frame(new_window)
        frame_enc.pack()

        img_user = Image.open("user.png")
        img_render = ImageTk.PhotoImage(img_user.resize((50,50)))
        label_img = Label(frame_enc, image=img_render)
        label_img.image = img_render
        label_img.grid(row=0,column=0,padx=20,pady=50)

        Label(frame_enc,text=f"Bienvenido {nickname}",font=("Comic Sans",25)).grid(row=0,column=1,pady=50)

        new_window.mainloop()

    def abrir_registro(self):
        VentanaRegistro(self.root, self.db)

# ==============================
# CLASE REGISTRO DE USUARIOS
# ==============================

class VentanaRegistro:
    def __init__(self, parent, db):
        self.db = db
        self.top = Toplevel(parent)
        self.top.title("Registrar nuevo usuario")
        self.top.geometry("400x420")
        self.top.resizable(0,0)

        Label(self.top, text="REGISTRO DE USUARIO", font=("Comic Sans", 16)).pack(pady=20)

        frame = Frame(self.top)
        frame.pack()

        Label(frame,text="Nickname:",font=("Comic Sans", 13)).grid(row=0,column=0,pady=10)
        self.nick = Entry(frame,width=25,font=("Comic Sans", 13))
        self.nick.grid(row=0,column=1,pady=10)

        Label(frame,text="Contraseña:",font=("Comic Sans", 13)).grid(row=1,column=0,pady=10)
        self.passw = Entry(frame,show="*",width=25,font=("Comic Sans", 13))
        self.passw.grid(row=1,column=1,pady=10)

        Label(frame,text="Fecha nacimiento (YYYY-MM-DD):",font=("Comic Sans", 11)).grid(row=2,column=0,columnspan=2,pady=10)
        self.birth = Entry(frame,width=25,font=("Comic Sans", 13))
        self.birth.grid(row=3,column=0,columnspan=2,pady=5)

        Button(frame,text="Registrar",command=self.registrar_usuario,bg="black",fg="white",
               font=("Comic Sans",13),width=12).grid(row=4,column=0,columnspan=2,pady=20)

    def registrar_usuario(self):
        nick = self.nick.get().strip()
        passw = self.passw.get().strip()
        birth = self.birth.get().strip()

        if not nick or not passw or not birth:
            messagebox.showwarning("Aviso", "Rellena todos los campos.")
            return

        ok = self.db.insertar_usuario(nick, passw, birth, blocked=False)
        if ok:
            messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
            self.top.destroy()
            data = self.db.validar_usuario(nick, passw)
            abrir_programa_directo(data[1])  # ✅ nueva forma correcta
        else:
            messagebox.showerror("Error", "El usuario ya existe.")


# ==============================
# FUNCIÓN GLOBAL: ABRIR PROGRAMA
# ==============================

def abrir_programa_directo(nickname):
    """Abre directamente la ventana del programa sin depender de VentanaLogin."""
    new_window = Tk()
    new_window.title("Acceso al programa")
    new_window.geometry("600x400")

    frame_enc = Frame(new_window)
    frame_enc.pack()

    img_user = Image.open("user.png")
    img_render = ImageTk.PhotoImage(img_user.resize((50, 50)))
    label_img = Label(frame_enc, image=img_render)
    label_img.image = img_render
    label_img.grid(row=0, column=0, padx=20, pady=50)

    Label(frame_enc, text=f"Bienvenido {nickname}", font=("Comic Sans", 25)).grid(row=0, column=1, pady=50)

    new_window.mainloop()


# ==============================
# EJECUCIÓN PRINCIPAL
# ==============================

if __name__ == "__main__":
    root = Tk()
    app = VentanaLogin(root)
    root.mainloop()
