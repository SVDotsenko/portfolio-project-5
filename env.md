clean html unused styles
защита роутов

continue from 44 lesson

rename this file to env.py, and insert your data, remove this line
import os

os.environ.setdefault("DATABASE_URL", "postgres://insert your data here")
os.environ.setdefault("SECRET_KEY", "insert your data here")
os.environ.setdefault("CLOUDINARY_URL", "cloudinary://insert your data here")
