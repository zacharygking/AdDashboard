# AdDashboard
Dashboard for management of campaign data

Welcome to the Ad Report Dashboard. This application is built on top of Django and automatically generates Advertisement Campaign reports based on your Google Adwords and Facebook Marketing Data. If you would like to check out the application live it is currently live at http://addashboard.idmloco3.webfactional.com/ however both a facebook marketing enabled account and google adwords account are required in order for the API to fetch the data.

---

If you are looking for a quick overview of this project for assessment purposes the following files contain
the most vital sections of code:

1. Templating/Bootstrap
  * report/templates/report/grandview.html
  * report/templates/report/select.html
2. API usage/backend development
  * report/views.py
3. URL/regex 
  * report/urls.py
  * adwords/urls.py

---
# Developer Notes
Dependencies <br>
-googleads <br>
-facebookads <br>
-django <br>
-django-allauth <br>
-django-excel <br>
-pyexcel-xls <br>

webfaction setup:

	create application: Django 1.8.4 (mod_wsgi 4.4.13/Python 2.7)

ssh: 

	cd $HOME/lib/python2.7
	easy_install-2.7 pip
	pip2.7 install django-allauth
	pip2.7 install pyexcel-xls
	pip2.7 install django-excel
	pip2.7 install facebookads
	pip2.7 install googleads

	git project into myproject folder

	update apache2/bin/httpd.conf for myproject/adwords/wsgi.py


still not sure where to put yaml file?

	- yaml file save at /root of website or actually user home dir?



