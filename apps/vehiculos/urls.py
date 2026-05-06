from django.urls import path
from . import views

app_name = 'vehiculos'

urlpatterns = [
    path('', views.vehiculo_list, name='lista'),
    path('nuevo/', views.vehiculo_create, name='crear'),
    path('<int:pk>/editar/', views.vehiculo_update, name='editar'),
]
