from django.urls import path
from . import views

app_name = 'mantenimiento'

urlpatterns = [
    path('alertas/', views.alerta_list, name='alertas'),
    path('alertas/<int:pk>/notificar/', views.alerta_notificar, name='notificar'),
]
