from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('usuarios/', views.usuario_list, name='usuarios_lista'),
    path('usuarios/nuevo/', views.usuario_create, name='usuario_crear'),
    path('usuarios/<int:pk>/editar/', views.usuario_update, name='usuario_editar'),
]
