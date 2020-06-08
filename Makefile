# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Mon Jun 08, 2020 at 11:28 PM +0800

.PHONY: sdist install test unittest

sdist:
	@python ./setup.py sdist

install:
	@python ./setup.py install

clean:
	@rm -rf ./dist
	@rm -rf ./pyTuplingUtils.egg-info
	@rm -rf ./build

test: unittest

##############
# Unit tests #
##############

unittest:
	@coverage run -m unittest discover -s ./test
