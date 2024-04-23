"""
Settings file to be used during testing
"""
from .settings import *

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"