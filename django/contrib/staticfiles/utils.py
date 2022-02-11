import os
import fnmatch
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

def is_ignored(path, ignore_patterns=[]):
    """
    Return True or False depending on whether the ``path`` should be
    ignored (if it matches any pattern in ``ignore_patterns``).
    """
    return any(fnmatch.fnmatchcase(path, pattern) for pattern in ignore_patterns)

def get_files(storage, ignore_patterns=[], location=''):
    """
    Recursively walk the storage directories yielding the paths
    of all files that should be copied.
    """
    directories, files = storage.listdir(location)
    for fn in files:
        if is_ignored(fn, ignore_patterns):
            continue
        if location:
            fn = os.path.join(location, fn)
        yield fn
    for dir in directories:
        if is_ignored(dir, ignore_patterns):
            continue
        if location:
            dir = os.path.join(location, dir)
        yield from get_files(storage, ignore_patterns, dir)

def check_settings():
    """
    Checks if the staticfiles settings have sane values.

    """
    if not settings.STATIC_URL:
        raise ImproperlyConfigured(
            "You're using the staticfiles app "
            "without having set the required STATIC_URL setting.")
    if settings.MEDIA_URL == settings.STATIC_URL:
        raise ImproperlyConfigured("The MEDIA_URL and STATIC_URL "
                                   "settings must have different values")
    if ((settings.MEDIA_ROOT and settings.STATIC_ROOT) and
            (settings.MEDIA_ROOT == settings.STATIC_ROOT)):
        raise ImproperlyConfigured("The MEDIA_ROOT and STATIC_ROOT "
                                   "settings must have different values")
