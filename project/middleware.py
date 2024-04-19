# project/middleware.py

from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin

class BasicAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_authenticated and request.path != '/login/':
            if 'HTTP_AUTHORIZATION' in request.META:
                auth = request.META['HTTP_AUTHORIZATION'].split()
                if len(auth) == 2:
                    if auth[0].lower() == 'basic':
                        username, password = auth[1].decode('base64').split(':')
                        user = authenticate(username=username, password=password)
                        if user is not None:
                            if user.is_active:
                                login(request, user)
                                return None
            return HttpResponse('Unauthorized', status=401)
