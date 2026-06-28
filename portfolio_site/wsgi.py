"""WSGI config for portfolio_site project.

WhiteNoise wraps the Django application so static files are served without a
dedicated web server -- handy on PythonAnywhere and in development alike.
"""
import os

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portfolio_site.settings")

application = get_wsgi_application()
application = WhiteNoise(application)
