from django.urls import path
from . import views

app_name = 'ordenes'

urlpatterns = [
    path('', views.orden_list, name='lista'),
    path('nueva/', views.orden_create, name='crear'),
    path('<int:pk>/', views.orden_detalle, name='detalle'),
    path('<int:pk>/editar/', views.orden_update, name='editar'),
    path('<int:pk>/iniciar/', views.orden_iniciar, name='iniciar'),
    path('<int:pk>/completar/', views.orden_completar, name='completar'),
    path('<int:pk>/facturar/', views.orden_facturar, name='facturar'),
    path('<int:pk>/servicios/agregar/', views.servicio_add, name='servicio_agregar'),
    path('<int:pk>/productos/agregar/', views.producto_add, name='producto_agregar'),
    path('servicios/<int:pk>/eliminar/', views.servicio_delete, name='servicio_eliminar'),
    path('productos/<int:pk>/eliminar/', views.producto_delete, name='producto_eliminar'),
]
