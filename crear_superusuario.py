"""
Script para crear superusuario por defecto del sistema.
Ejecutar: python crear_superusuario.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configuracion.settings')
django.setup()

from apps.accounts.models import Usuario

# ─────────────────────────────────────────────
# Superusuario (Dueño del taller)
# ─────────────────────────────────────────────
SUPERUSER_DATA = {
    'username': 'admin',
    'email': 'admin@taller.com',
    'nombre_completo': 'Administrador General',
    'rol': 'DUENO',
    'password': 'admin1234',
}

# ─────────────────────────────────────────────
# Usuarios de ejemplo adicionales
# ─────────────────────────────────────────────
USUARIOS_EJEMPLO = [
    {
        'username': 'gerente',
        'email': 'gerente@taller.com',
        'nombre_completo': 'María García',
        'rol': 'ADMINISTRADOR',
        'password': 'admin1234',
    },
    {
        'username': 'mecanico1',
        'email': 'mecanico1@taller.com',
        'nombre_completo': 'Juan Pérez',
        'rol': 'MECANICO',
        'password': 'admin1234',
    },
]


def crear_usuarios():
    # Superusuario / Dueno
    if not Usuario.objects.filter(username=SUPERUSER_DATA['username']).exists():
        u = Usuario.objects.create_superuser(**SUPERUSER_DATA)
        print(f"[OK] Superusuario creado: {u.username} / {SUPERUSER_DATA['password']}")
    else:
        print(f"[INFO] Superusuario '{SUPERUSER_DATA['username']}' ya existe")

    # Usuarios de ejemplo
    for datos in USUARIOS_EJEMPLO:
        pwd = datos.pop('password')
        if not Usuario.objects.filter(username=datos['username']).exists():
            u = Usuario.objects.create_user(password=pwd, **datos)
            print(f"[OK] Usuario creado: {u.username} ({u.get_rol_display()}) / {pwd}")
        else:
            print(f"[INFO] Usuario '{datos['username']}' ya existe")
        datos['password'] = pwd  # restore for idempotence

    print("\n[ACCESO] Panel de administracion:")
    print(f"   URL: http://127.0.0.1:8000/admin/")
    print(f"   Usuario: {SUPERUSER_DATA['username']}")
    print(f"   Contrasena: {SUPERUSER_DATA['password']}")


if __name__ == '__main__':
    crear_usuarios()
