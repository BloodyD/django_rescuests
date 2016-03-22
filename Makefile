install:
	python setup.py install

test: install
	cd tests && python manage.py test

deploy:
	python setup.py sdist upload -r pypi
