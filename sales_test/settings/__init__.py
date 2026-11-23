import os
from decouple import config

environment = config('DJANGO_ENV', default='production')

if environment == 'production':
    from .production import *
else:
    from .development import *