from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    path('', views.producto_list, name='lista'),
    path('repuestos/', views.repuesto_list, name='repuestos'),
    path('repuestos/nuevo/', views.repuesto_create, name='repuesto_crear'),
    path('repuestos/<int:pk>/editar/', views.repuesto_update, name='repuesto_editar'),
    path('neumaticos/', views.neumatico_list, name='neumaticos'),
    path('neumaticos/nuevo/', views.neumatico_create, name='neumatico_crear'),
    path('neumaticos/<int:pk>/editar/', views.neumatico_update, name='neumatico_editar'),
]
