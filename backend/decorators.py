from django.shortcuts import redirect
from functools import wraps

def admin_only(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.user_type == "Admin":
            return view_func(request, *args, **kwargs)
        return redirect('frontend_login')
    return wrapper