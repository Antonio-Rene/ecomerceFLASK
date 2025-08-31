
import sys
import os


project_home = os.path.expanduser('~/ecommerce_flask_bootstrap')
if project_home not in sys.path:
    sys.path.insert(0, project_home)


os.environ['FLASK_ENV'] = 'production'


from app import app as application
