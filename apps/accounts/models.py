from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class UsuarioManager(BaseUserManager):
    def create_user(self, username, email, nombre_completo, rol, password=None, **extra):
        if not username:
            raise ValueError('El nombre de usuario es obligatorio')
        email = self.normalize_email(email)
        user = self.model(
            username=username, email=email,
            nombre_completo=nombre_completo, rol=rol, **extra
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, nombre_completo, rol='DUENO', password=None, **extra):
        extra.setdefault('is_staff', True)
        extra.setdefault('is_superuser', True)
        return self.create_user(username, email, nombre_completo, rol, password, **extra)


class Usuario(AbstractBaseUser, PermissionsMixin):
    class Rol(models.TextChoices):
        DUENO = 'DUENO', 'Dueño'
        ADMINISTRADOR = 'ADMINISTRADOR', 'Administrador'
        MECANICO = 'MECANICO', 'Mecánico'

    username = models.CharField(max_length=50, unique=True, verbose_name='Nombre de Usuario')
    email = models.EmailField(max_length=100, unique=True, verbose_name='Email')
    nombre_completo = models.CharField(max_length=100, verbose_name='Nombre Completo')
    rol = models.CharField(max_length=20, choices=Rol.choices, verbose_name='Rol')
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    is_staff = models.BooleanField(default=False, verbose_name='Staff')
    fecha_creacion = models.DateTimeField(default=timezone.now, verbose_name='Fecha de Creación')
    fecha_ultimo_acceso = models.DateTimeField(blank=True, null=True, verbose_name='Último Acceso')
    debe_cambiar_password = models.BooleanField(default=False, verbose_name='Debe Cambiar Contraseña')

    objects = UsuarioManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'nombre_completo']

    class Meta:
        db_table = 'usuario'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        indexes = [
            models.Index(fields=['username'], name='idx_usuario_username'),
            models.Index(fields=['rol'], name='idx_usuario_rol'),
        ]

    def __str__(self):
        return f"{self.nombre_completo} ({self.get_rol_display()})"
