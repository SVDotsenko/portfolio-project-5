add tooltips
validation with toottips
copy card number to clipboard before entering the donation page, and show tooltip
add spiner to donation button
on history page add section with donators
dollar sign left from input goal

clean css, html unused styles

continue from 44 lesson

rename this file to env.py, and insert your data, remove this line
import os

os.environ.setdefault("DATABASE_URL", "postgres://insert your data here")
os.environ.setdefault("SECRET_KEY", "insert your data here")
os.environ.setdefault("CLOUDINARY_URL", "cloudinary://insert your data here")
