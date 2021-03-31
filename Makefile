# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Wed Mar 31, 2021 at 11:21 PM +0200

.PHONY: sdist install install-egg clean \
	unittest unittest-local

sdist:
	@python ./setup.py sdist

install:
	@pip install . --force-reinstall

install-egg:
	@python ./setup.py install

clean:
	@rm -rf ./dist
	@rm -rf ./pyTuplingUtils.egg-info
	@rm -rf ./build

##############
# Unit tests #
##############

unittest:
	@coverage run -m unittest discover -s ./test

unittest-local:
	@python -m unittest discover -s ./test
