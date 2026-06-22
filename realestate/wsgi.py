"""
WSGI config for realestate project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

# Vercel paths lookup pipeline patch
path0 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if path0 not in sys.path:
    sys.path.append(path0)

# 🚨 APNE PROJECT KA NAAM YAHAN SENSE KARIYE (e.g., 'core.settings' ya 'DigiEstate.settings')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = get_wsgi_application()

# App handle exposure for Vercel Serverless Functions
app = application
