from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ('username', 'nombre_completo', 'email', 'rol', 'is_active', 'is_staff', 'fecha_creacion')
    list_filter = ('rol', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'nombre_completo')
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informacion Personal', {'fields': ('nombre_completo', 'email')}),
        ('Rol y Permisos', {'fields': ('rol', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Acceso', {'fields': ('fecha_ultimo_acceso', 'debe_cambiar_password')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'nombre_completo', 'rol', 'password1', 'password2'),
        }),
    )
    readonly_fields = ('fecha_ultimo_acceso',)
