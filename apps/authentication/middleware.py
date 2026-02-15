import re

from django.shortcuts import redirect


class LoginRequiredMiddleware:
    EXEMPT_URLS = (
        "/login/",
        "/logout/",
        "/register/",
        "/admin/",
        "/booking/",
        r"^/booking/\d+/confirmation/$",
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        path = request.path

        for pattern in self.EXEMPT_URLS:
            if re.match(pattern, path):
                return self.get_response(request)

        if not request.user.is_authenticated:
            return redirect("/login/")

        return self.get_response(request)