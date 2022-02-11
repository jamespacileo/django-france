"""
A set of request processors that return dictionaries to be merged into a
template context. Each function takes the request object as its only parameter
and returns a dictionary to add to the context.

These are referenced from the setting TEMPLATE_CONTEXT_PROCESSORS and used by
RequestContext.
"""

from django.conf import settings
from django.middleware.csrf import get_token
from django.utils.functional import lazy

def csrf(request):
    """
    Context processor that provides a CSRF token, or the string 'NOTPROVIDED' if
    it has not been provided by either a view decorator or the middleware
    """
    def _get_val():
        token = get_token(request)
        return 'NOTPROVIDED' if token is None else token
    _get_val = lazy(_get_val, str)

    return {'csrf_token': _get_val() }

def debug(request):
    "Returns context variables helpful for debugging."
    context_extras = {}
    if settings.DEBUG and request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS:
        context_extras['debug'] = True
        from django.db import connection
        context_extras['sql_queries'] = connection.queries
    return context_extras

def i18n(request):
    from django.utils import translation

    context_extras = {
        'LANGUAGES': settings.LANGUAGES,
        'LANGUAGE_CODE': translation.get_language(),
    }

    context_extras['LANGUAGE_BIDI'] = translation.get_language_bidi()

    return context_extras

def static(request):
    """
    Adds static-related context variables to the context.

    """
    return {'STATIC_URL': settings.STATIC_URL}

def media(request):
    """
    Adds media-related context variables to the context.

    """
    return {'MEDIA_URL': settings.MEDIA_URL}

def request(request):
    return {'request': request}

# PermWrapper and PermLookupDict proxy the permissions system into objects that
# the template system can understand. They once lived here -- they have
# been moved to django.contrib.auth.context_processors.

from django.contrib.auth.context_processors import PermLookupDict as RealPermLookupDict
from django.contrib.auth.context_processors import PermWrapper as RealPermWrapper

class PermLookupDict(RealPermLookupDict):
    def __init__(self, *args, **kwargs):
        import warnings
        warnings.warn(
            "`django.core.context_processors.PermLookupDict` is " \
            "deprecated; use `django.contrib.auth.context_processors.PermLookupDict` " \
            "instead.",
            DeprecationWarning
        )
        super(PermLookupDict, self).__init__(*args, **kwargs)

class PermWrapper(RealPermWrapper):
    def __init__(self, *args, **kwargs):
        import warnings
        warnings.warn(
            "`django.core.context_processors.PermWrapper` is " \
            "deprecated; use `django.contrib.auth.context_processors.PermWrapper` " \
            "instead.",
            DeprecationWarning
        )
        super(PermWrapper, self).__init__(*args, **kwargs)
