#!/usr/bin/env python3
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Thu Jun 18, 2020 at 01:44 AM +0800

import numpy as np


KNOWN_SYMB = {
    # Units
    'MeV': 1.0,
    'GeV': 1000.0,
    # Particle masses
    # B mesons
    'PDG_M_B0': 5279.64,
    # D mesons
    'PDG_M_Dst': 2010.26,
    'PDG_M_D0': 1864.83,
}

KNOWN_FUNC = {
    'ABS': np.abs,
}
