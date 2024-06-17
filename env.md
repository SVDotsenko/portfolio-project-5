readme
	Стили в цсс почистить когда буду делать описание в ридми. в части валидации цсс
	check names for html elements, they should describe the content
	unit-test
	fb


rename this file to env.py, and insert your data, remove this line
import os

os.environ.setdefault("DATABASE_URL", "postgres://insert your data here")
os.environ.setdefault("SECRET_KEY", "insert your data here")
os.environ.setdefault("CLOUDINARY_URL", "cloudinary://insert your data here")
