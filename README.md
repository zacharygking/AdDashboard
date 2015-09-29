# AdDashboard
Dashboard for management of campaign data

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



