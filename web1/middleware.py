from django.shortcuts import redirect
from django.conf import settings

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and not request.path.startswith(settings.LOGIN_URL):
            return redirect(settings.LOGIN_URL)
        response = self.get_response(request)
        return response