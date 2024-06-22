rename this file to env.py, and insert your data, remove this line
import os

os.environ.setdefault("DATABASE_URL", "postgres://insert your data here")
os.environ.setdefault("SECRET_KEY", "insert your data here")
os.environ.setdefault("STRIPE_PK", "insert your data here")
os.environ.setdefault("STRIPE_SK", "insert your data here")
os.environ.setdefault("DEVELOPMENT", "") # just leave this line as is, and remove this comment. This line is used to 
check if the app is in development mode. If you need to run application in production mode, just remove this line or 
change DEBUG = False in settings.py