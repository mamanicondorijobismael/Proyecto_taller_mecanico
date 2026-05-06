from django.urls import path
from . import views

app_name = 'reportes'

urlpatterns = [
    path('', views.reportes_dashboard, name='dashboard'),
    path('inventario/', views.reporte_inventario, name='inventario'),
    path('producto/<int:pk>/', views.reporte_producto, name='producto_detalle'),
]
