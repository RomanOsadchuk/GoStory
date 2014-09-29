from functools import wraps
from django.http import HttpResponseForbidden


def ajax_only(f):
    @wraps(f)
    def wrapper(request, *args, **kwargs):
         if not request.is_ajax():
             return HttpResponseForbidden('This page available only via ajax')
         return f(request, *args, **kwargs)
    return wrapper

