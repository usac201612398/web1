# web1/middleware.py
import re
from django.conf import settings
from django.shortcuts import redirect

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_urls = [re.compile(expr) for expr in getattr(settings, "LOGIN_EXEMPT_URLS", [])]

    def __call__(self, request):
        path = request.path_info.lstrip('/')
        
        # Si la URL está en la lista de exentas, pasar
        if any(m.match(path) for m in self.exempt_urls):
            return self.get_response(request)
        
        # Si el usuario no está autenticado, redirigir a login
        if not request.user.is_authenticated:
            return redirect(settings.LOGIN_URL)
        
        return self.get_response(request)