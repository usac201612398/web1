# web1/middleware.py
import re
from django.conf import settings
from django.shortcuts import redirect

class LoginRequiredMiddleware:
    """
    Middleware que exige login excepto para URLs exentas (webhooks, etc).
    Compatible con django_auth_adfs.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_urls = [re.compile(expr) for expr in getattr(settings, "LOGIN_EXEMPT_URLS", [])]

    def __call__(self, request):
        path = request.path_info.lstrip('/')

        # Excluir rutas de webhook o públicas
        if any(m.match(path) for m in self.exempt_urls):
            return self.get_response(request)

        # Si no está autenticado, redirigir a ADFS login
        if not request.user.is_authenticated:
            return redirect(settings.LOGIN_URL)

        return self.get_response(request)