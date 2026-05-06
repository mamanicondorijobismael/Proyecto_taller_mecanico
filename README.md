# Proyecto Mecánico (Django)

Aplicación web hecha con Django para gestión de un taller (clientes, vehículos, inventario, órdenes, etc.).

## Requisitos

- Python 3.13+
- pip

Las dependencias del proyecto están en `requirements.txt`.

## Instalación (Windows)

1) Crear y activar entorno virtual (si no lo tienes):

```powershell
python -m venv entorno
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\entorno\Scripts\Activate.ps1
```

1) Instalar dependencias:

```powershell
pip install -r requirements.txt
```

## Configuración

- Este proyecto usa SQLite por defecto.
- El archivo `db.sqlite3` NO se sube a GitHub (está en `.gitignore`).
- Si usas variables de entorno, crea un archivo `.env` (también ignorado por git).

## Migraciones y arranque

```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Luego abre: <http://127.0.0.1:8000/>

## Crear superusuario

```powershell
python manage.py createsuperuser
```

También existe el script `crear_superusuario.py` (si lo estás usando en tu flujo), pero la forma estándar es el comando de Django.

## Datos iniciales (seed)

Si necesitas cargar categorías u otros datos iniciales:

```powershell
python seed_categorias.py
```

## Estructura del proyecto

- `configuracion/`: configuración principal (settings, urls, wsgi/asgi)
- `apps/`: apps del dominio
  - `accounts/`, `clientes/`, `vehiculos/`, `inventario/`, `ordenes/`, `facturas/`, `reservas/`, `reportes/`, `mantenimiento/`
- `templates/`: plantillas HTML
- `static/`: archivos estáticos del proyecto
- `media/`: archivos subidos por usuarios (se ignora en git)
- `logs/`: logs locales (se ignora en git)

## Notas de git

Lo que no se debe subir a GitHub ya está cubierto en `.gitignore`, incluyendo:

- `entorno/` (venv)
- `db.sqlite3`
- `media/`
- `logs/`
- `.env`

## Comandos útiles

```powershell
python manage.py check
python manage.py test
```
