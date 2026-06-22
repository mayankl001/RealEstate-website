import os
import sys
from django.core.wsgi import get_wsgi_application

# 📁 Isse project root directory system path me force-inject ho jayegi
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# 🚀 Strict deployment settings link
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realestate.settings')

application = get_wsgi_application()

# 🚨 Vercel standard handler linkage
app = application