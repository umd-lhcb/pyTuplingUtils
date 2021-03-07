# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Sun Mar 07, 2021 at 09:12 PM +0100

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

unittest-local:
	@python -m unittest discover -s ./test
