# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Fri May 01, 2020 at 01:41 AM +0800

.PHONY: sdist install test unittest

sdist:
	@python ./setup.py sdist

install:
	@python ./setup.py install

clean:
	@rm -rf ./dist
	@rm -rf ./pyBabyMaker.egg-info

test: unittest

##############
# Unit tests #
##############

unittest:
	@coverage run -m unittest discover -s ./test
