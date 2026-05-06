from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

def rol_requerido(roles):
    """
    Decorator for views that checks if the user has one of the required roles.
    Example: @rol_requerido(['DUENO', 'ADMINISTRADOR'])
    """
    def check_role(user):
        if user.is_authenticated and (user.rol in roles or user.is_superuser):
            return True
        raise PermissionDenied
    return user_passes_test(check_role)

def es_dueno(user):
    return user.is_authenticated and (user.rol == 'DUENO' or user.is_superuser)

def es_admin(user):
    return user.is_authenticated and (user.rol in ['DUENO', 'ADMINISTRADOR'] or user.is_superuser)

def es_mecanico(user):
    return user.is_authenticated and (user.rol in ['DUENO', 'ADMINISTRADOR', 'MECANICO'] or user.is_superuser)
