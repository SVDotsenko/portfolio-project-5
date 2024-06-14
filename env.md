Include a sitemap on your application to allow search engine bot crawling
Include a robots.txt file to control search engine bot crawling

readme
	Include Meta Description tags in the application HTML	
	check names for html elements, they should describe the content	
	fb
	unit-test
	scrum
	Стили в цсс почистить когда буду делать описание в ридми. в части валидации цсс
	Document the e-commerce business model underlying your application


rename this file to env.py, and insert your data, remove this line
import os

os.environ.setdefault("DATABASE_URL", "postgres://insert your data here")
os.environ.setdefault("SECRET_KEY", "insert your data here")
os.environ.setdefault("CLOUDINARY_URL", "cloudinary://insert your data here")
