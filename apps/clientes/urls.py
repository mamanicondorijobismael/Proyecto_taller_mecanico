from django.urls import path
from . import views

app_name = 'clientes'

urlpatterns = [
    path('', views.cliente_list, name='lista'),
    path('nuevo/', views.cliente_create, name='crear'),
    path('<int:pk>/editar/', views.cliente_update, name='editar'),
]
