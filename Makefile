# Author: Yipeng Sun <syp at umd dot edu>
# License: BSD 2-clause
# Last Change: Mon Jun 14, 2021 at 05:25 AM +0200

.PHONY: sdist install install-egg clean \
	unittest unittest-local integrationtest

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
	@rm ./*.png

##############
# Unit tests #
##############

unittest:
	@coverage run -m unittest discover -s ./test

unittest-local:
	@python -m unittest discover -s ./test

integrationtest:
	@plotbr \
		-n ./samples/sample.root/TupleB0/DecayTree -b Dst_2010_minus_PT D0_PT \
		-l "\$$D^{*-}\$$ \$$p_T\$$" "\$$D^0\$$ \$$p_T\$$" \
		--cuts "Dst_2010_minus_PT < 8000" "true" \
		-n ./samples/sample.root/TupleB0/DecayTree -b Dst_2010_minus_TRUEPT D0_TRUEPT \
		-l "\$$D^{*-}\$$ \$$p_T\$$ (true)" "\$$D^0\$$ \$$p_T\$$ (true)" \
		--cuts "Dst_2010_minus_PT < 8000" "true" \
		-XD 1000 1e4 \
		-XL "Transverse momentum (meas./MC true)" \
		--debug \
		-o test_plotbr.png
	@plotbrdiff \
		-n ./samples/sample.root/TupleB0/DecayTree -b Dst_2010_minus_PT \
		--ref-cuts "Dst_2010_minus_PT < 8000" \
		-N ./samples/sample.root/TupleB0/DecayTree -B Dst_2010_minus_TRUEPT \
		-l "\$$D^{*-}\$$ \$$p_T\$$ (meas-MC true)" \
		-XL "Transverse momentum (meas./MC true)" \
		--debug \
		-o test_plotbrdiff.png
