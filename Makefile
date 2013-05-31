.PHONY: build
build: distribute_setup.py
	python setup.py sdist

distribute_setup.py:
	curl -O http://python-distribute.org/distribute_setup.py
	