from django.http.response import HttpResponseForbidden
from django.shortcuts import redirect



def isAdmin(message=None):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if  request.user.is_authenticated and (request.user.is_admin or request.user.is_superuser):
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponseForbidden(message)
        return wrapper
    return decorator


def noAuth(message=None):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs): 
            if  request.user.is_authenticated:
                return redirect('base:index')
            else:
                return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


# def permissionRequired(message=None):
#     def decorator(view_func):
#         def wrapper(request, *args, **kwargs): 
#             if  request.user.permissions.filter('as'):
#                 return HttpResponseForbidden(message)
#             else:
#                 return view_func(request, *args, **kwargs)
#         return wrapper
#     return decorator

