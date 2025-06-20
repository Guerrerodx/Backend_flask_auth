# Backend Flask Auth

Sistema backend desarrollado en Flask que permite gestionar usuarios con autenticación basada en JWT. Incluye roles, control de acceso, y endpoints protegidos para perfiles y administración.

## 🔧 Estructura del Proyecto

```
backend_flask_auth/
│
├── app/
│   ├── routes/
│   │   ├── __init__.py
│   │   └── auth.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── jwt.py
│   │   └── models.py
│   └── users.json
├── run.py
├── requirements.txt
└── README.md
```

## ▶️ Requisitos

* Python 3.8+
* Flask

Instalación de dependencias:

```bash
pip install -r requirements.txt
```

## 🚀 Ejecución

```bash
python run.py
```

El servicio estará disponible en: `http://127.0.0.1:5000/`

---

## 🔐 Endpoints

### Autenticación

#### `POST /auth/register`

Registra un nuevo usuario.

* **Body JSON:**

```json
{
  "username": "nuevo",
  "password": "123456"
}
```

* Para registrar un usuario con rol admin se debe agregar `"role": "admin"` y estar autenticado como admin.

#### `POST /auth/login`

Genera un token JWT válido.

* **Body JSON:**

```json
{
  "username": "usuario",
  "password": "123456"
}
```

#### `POST /auth/logout`

Cierra la sesión (token inválido a partir de ahora).

* **Headers:**

```
Authorization: <token>
```

#### `GET /auth/profile`

Devuelve los datos del usuario autenticado.

* **Headers:**

```
Authorization: <token>
```

#### `GET /auth/admin/dashboard`

Devuelve información exclusiva para administradores.

* **Headers:**

```
Authorization: <token>
```

#### `DELETE /auth/admin/delete/<id>`

Elimina un usuario por ID (requiere token de admin).

#### `POST /auth/change-password`

Permite a un usuario cambiar su propia contraseña.

* **Body JSON:**

```json
{
  "old_password": "123456",
  "new_password": "nueva123"
}
```

* **Headers:**

```
Authorization: <token>
```

---

## 📁 Persistencia

* Los usuarios se almacenan en `app/utils/users.json`.
* Los tokens revocados se almacenan en memoria temporal (no persistente).
* El ID de usuario se autoincrementa según el ID más alto actual en el archivo JSON.

---

## 🧪 Pruebas

### Postman

Se incluye una colección de Postman (collection.postman.json) para facilitar la prueba de todos los endpoints. Puedes importarla directamente en Postman.

---

## 📝 Consideraciones

* Este proyecto es una base funcional para pruebas y enseñanza.
* No implementa encriptación de contraseñas (se puede agregar con `werkzeug.security`).
* No incluye base de datos; usa archivos `.json` para simplicidad.

## 👤 Autor

Camilo Guerrero