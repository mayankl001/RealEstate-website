import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realestate.settings')

application = get_wsgi_application()

# WhiteNoise ko manually WSGI application ke upar wrap karein
# Isse Vercel bina kisi build script ke aapki CSS serve karne lagega
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
application = WhiteNoise(application, root=os.path.join(base_dir, 'staticfiles'))
application.add_files(os.path.join(base_dir, 'static'), prefix='')