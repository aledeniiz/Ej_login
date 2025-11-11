1️⃣ DESCRIPCIÓN GENERAL
-----------------------------------------------------
Esta aplicación implementa un sistema completo de registro y acceso de usuarios
utilizando interfaz gráfica (Tkinter) y una base de datos SQLite. 

Se ha sustituido el uso del archivo users_dict.py del ejemplo original por una 
base de datos local (users.db), asegurando persistencia de datos y mejor gestión
de usuarios.

El diseño mantiene el estilo visual del ejemplo proporcionado por el profesor,
con las imágenes login.png y user.png incluidas en el proyecto.


2️⃣ FUNCIONALIDADES PRINCIPALES
-----------------------------------------------------
- Ventana de LOGIN con validación de credenciales.
- Ventana de REGISTRO de nuevos usuarios (enlazada desde el login).
- Al registrarse correctamente, el usuario queda logueado automáticamente.
- Almacenamiento de datos con SQLite (tabla "usuarios").
- Contraseñas encriptadas mediante hash MD5 (hashlib).
- Control de acceso con excepciones personalizadas:
    · MenorEdadError: si el usuario es menor de 18 años.
    · UsuarioBloqueadoError: si el usuario está bloqueado.
- Mensajes informativos con tkinter.messagebox.
- Interfaz amigable y clara con fuentes y estilos Comic Sans.


3️⃣ ESTRUCTURA DEL PROYECTO
-----------------------------------------------------
Ejercicio Login/
│
├── Ej_final.py            → Archivo principal de la aplicación.
├── login.png              → Icono de cabecera en la ventana de login.
├── user.png               → Icono de bienvenida en la ventana de acceso.
├── users.db               → Base de datos SQLite con los usuarios.
└── README.txt             → Documento explicativo (este archivo).


4️⃣ USO DE LA APLICACIÓN
-----------------------------------------------------
1. Ejecutar el archivo Ej_final.py o app_login.py.
2. Aparecerá la ventana de inicio de sesión.
3. Si el usuario no existe, pulsar “Registrar nuevo usuario”.
4. Introducir:
     - Nickname (único)
     - Contraseña
     - Fecha de nacimiento (formato YYYY-MM-DD)
5. Tras registrarse, el usuario se conecta automáticamente.
6. Si es menor de edad o bloqueado, se lanza una excepción informativa.
7. Si los datos son correctos, se abre la ventana de bienvenida.


5️⃣ DETALLES TÉCNICOS
-----------------------------------------------------
- Base de datos: SQLite (users.db)
- Librerías usadas:
    · tkinter (interfaz gráfica)
    · hashlib (hash de contraseñas)
    · sqlite3 (persistencia de datos)
    · PIL (para mostrar imágenes)
- El programa crea automáticamente la base de datos si no existe.
- Cada contraseña se guarda en formato hash MD5.
- Los usuarios se identifican por el campo único "nickname".


6️⃣ CRÉDITOS Y OBSERVACIONES
-----------------------------------------------------
Desarrollo completamente original a partir del ejemplo facilitado en clase.
Cumple todos los requisitos solicitados en el enunciado:
· Persistencia con SQLite
· Encriptación de contraseñas
· Control de edad y bloqueo
· Interfaz gráfica funcional

Proyecto probado en Python 3.12 con entorno Visual Studio Code.
