\# 📋 Gestor de Proyectos y Tareas (Kanban)



Aplicación web de gestión de tareas personal inspirada en Trello, construida con Django.

Incluye tablero Kanban con arrastrar y soltar, dashboard de estadísticas, buscador,

etiquetas, subtareas y autenticación multiusuario.



> 🔗 \*\*Demo en vivo:\*\* \*(próximamente)\*

> 👤 \*\*Credenciales demo:\*\* `demo` / `demo1234`



\## ✨ Funcionalidades



\- ✅ CRUD completo de proyectos y tareas

\- 🧲 \*\*Tablero Kanban con drag \& drop\*\* (HTML5 drag \& drop + `fetch`/AJAX con CSRF)

\- 📊 Dashboard con estadísticas y gráfica (Chart.js)

\- 🔐 Registro, login y logout — cada usuario solo ve sus propios datos

\- 🔍 Buscador con filtros por texto, estado y etiqueta

\- 🏷️ Etiquetas de colores y subtareas con checklist

\- 🔔 Avisos de tareas por vencer / atrasadas (campanita)

\- ⏰ Comando `enviar\_recordatorios` con emails de aviso

\- 🌙 Modo oscuro persistente (localStorage)

\- 🛠️ Admin de Django configurado con inlines

\- 🎲 Comando `datos\_demo` para cargar datos de ejemplo



\## 🛠️ Stack tecnológico



\*\*Python · Django (MVT) · SQLite · Bootstrap 5 · JavaScript vanilla · Chart.js\*\*



\## 🚀 Ejecución local



```bash

git clone https://github.com/TU\_USUARIO/gestor-tareas-django.git

cd gestor-tareas-django

python -m venv venv

source venv/bin/activate      # Windows: venv\\Scripts\\activate

pip install -r requirements.txt

python manage.py migrate

python manage.py datos\_demo   # crea el usuario demo/demo1234 con datos

python manage.py runserver

```



Abre `http://127.0.0.1:8000` y entra con `demo` / `demo1234`.



\## 📚 Lo que aprendí construyéndolo



\- Patrón MVT de Django de punta a punta

\- Relaciones ORM: FK, M2M, `related\_name` y agregaciones (`Count`, `Avg`, `annotate`)

\- Autenticación con sesiones y permisos por objeto

\- Integración AJAX con Django (CSRF en peticiones `fetch`)

\- Context processors, management commands y ModelForms



\## ✍️ Autor



\*\*Scrodia\*\* · \[GitHub](https://github.com/TU\_USUARIO) · \[LinkedIn](https://linkedin.com/in/TU\_PERFIL)

