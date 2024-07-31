from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required

def group_required(*group_names):
    """
    Décorateur pour restreindre l'accès à une vue aux utilisateurs appartenant à certains groupes.
    
    Arguments:
    - group_names: liste des noms des groupes autorisés à accéder à la vue.
    """
    def decorator(view_function):
        @login_required  # Assure que l'utilisateur est connecté
        def _wrapped_view(request, *args, **kwargs):
            # Vérifie si l'utilisateur appartient à l'un des groupes spécifiés
            if request.user.groups.filter(name__in=group_names).exists():
                return view_function(request, *args, **kwargs)  # Appelle la vue si l'utilisateur est dans un des groupes
            raise PermissionDenied  # Lève une exception si l'utilisateur n'est pas dans les groupes autorisés
        return _wrapped_view
    return decorator

def permission_required(permission):
    """
    Décorateur pour restreindre l'accès à une vue aux utilisateurs ayant une certaine permission.
    
    Arguments:
    - permission: la permission requise pour accéder à la vue.
    """
    def decorator(view_function):
        @login_required  # Assure que l'utilisateur est connecté
        def _wrapped_view(request, *args, **kwargs):
            # Vérifie si l'utilisateur a la permission spécifiée
            if request.user.has_perm(permission):
                return view_function(request, *args, **kwargs)  # Appelle la vue si l'utilisateur a la permission
            raise PermissionDenied  # Lève une exception si l'utilisateur n'a pas la permission requise
        return _wrapped_view
    return decorator
