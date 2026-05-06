import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configuracion.settings')
django.setup()

from apps.inventario.models import CategoriaProducto

categorias = [
    {'nombre': 'Neumáticos de Verano', 'descripcion': 'Neumáticos para clima cálido'},
    {'nombre': 'Neumáticos de Invierno', 'descripcion': 'Neumáticos para nieve o frío extremo'},
    {'nombre': 'Neumáticos All Season', 'descripcion': 'Neumáticos para todo clima'},
    {'nombre': 'Frenos', 'descripcion': 'Pastillas, discos y balatas'},
    {'nombre': 'Filtros', 'descripcion': 'Filtros de aceite, aire y cabina'},
    {'nombre': 'Baterías', 'descripcion': 'Baterías automotrices'},
    {'nombre': 'Aceites y Lubricantes', 'descripcion': 'Aceites de motor, transmisión y grasas'},
    {'nombre': 'Suspensión', 'descripcion': 'Amortiguadores, bujes y rótulas'},
    {'nombre': 'Accesorios', 'descripcion': 'Accesorios generales para vehículos'},
]

print("Creando categorías por defecto...")
for cat_data in categorias:
    CategoriaProducto.objects.get_or_create(nombre=cat_data['nombre'], defaults={'descripcion': cat_data['descripcion']})
print("Categorías creadas exitosamente.")
