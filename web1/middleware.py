import re
from django.conf import settings
from django.shortcuts import redirect

class LoginRequiredMiddleware:
    """
    Middleware que exige login excepto para URLs exentas (webhooks, login, etc).
    Compatible con django_auth_adfs.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_urls = [re.compile(expr) for expr in getattr(settings, "LOGIN_EXEMPT_URLS", [])]

    def __call__(self, request):
        path = request.path_info  # deja la barra inicial
        if any(m.match(path) for m in self.exempt_urls):
            return self.get_response(request)

        if not request.user.is_authenticated:
            return redirect(settings.LOGIN_URL)

        return self.get_response(request)