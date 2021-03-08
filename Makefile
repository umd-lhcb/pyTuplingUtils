# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Mon Mar 08, 2021 at 01:15 AM +0100

.PHONY: sdist install test unittest

sdist:
	@python ./setup.py sdist

install:
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

unittest-local: install
	@python -m unittest discover -s ./test
