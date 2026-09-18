from functools import wraps

from django.http import HttpResponseForbidden


def funcao_requerida(*funcoes_permitidas):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            perfil = getattr(request.user, 'perfil', None)
            funcao = getattr(perfil, 'funcao', None) if perfil else None

            if funcao is None or funcao.nome not in funcoes_permitidas:
                return HttpResponseForbidden('Você não tem permissão para acessar esta página.')

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator