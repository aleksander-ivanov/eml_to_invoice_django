from .base import *

if os.environ.get('DJANGO_ENVIRONMENT') == 'Production':
    from .production import *
else:
    from .development import *
