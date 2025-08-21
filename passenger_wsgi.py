import sys
import os

# Add the project directory to the Python path
INTERP = os.path.expanduser("/home/username/virtualenv/property_management/3.9/bin/python")
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

# Set the environment to production
os.environ['FLASK_ENV'] = 'production'

# Import the Flask app
from app_production import app

# For cPanel deployment, the application should be available as 'application'
application = app

if __name__ == "__main__":
    application.run()