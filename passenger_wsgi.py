# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, '/var/www/u2621067/data/www/u2621067.isp.regruhosting.ru/calc')
sys.path.insert(1, '/var/www/u2621067/data/.venv/lib/python3.8/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'calc.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()