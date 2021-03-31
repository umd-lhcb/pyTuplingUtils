# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Wed Mar 31, 2021 at 10:58 PM +0200

.PHONY: sdist install test unittest

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
