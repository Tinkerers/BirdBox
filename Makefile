.PHONY: build clean
build: distribute_setup.py
	python setup.py sdist

distribute_setup.py:
	curl -O http://python-distribute.org/distribute_setup.py

clean:
	python setup.py clean
	rm -rf dist SmashPuttTwitterBox.egg-info distribute-*.tar.gz
