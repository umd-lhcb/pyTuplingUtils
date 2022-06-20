{ stdenv
, buildPythonPackage
, setuptools
, uproot
, lz4
, numpy
, matplotlib
, lark-parser
, mplhep
, tabulate
}:

buildPythonPackage rec {
  pname = "pyTuplingUtils";
  version = "0.3.3";

  src = builtins.path { path = ./..; name = pname; };

  preBuild = ''
    sed -i "s/0.0.1/${version}/" ./pyTuplingUtils/__init__.py
  '';

  propagatedBuildInputs = [
    setuptools
    uproot
    lz4
    matplotlib
    lark-parser
    mplhep
    tabulate
  ];

  doCheck = false;
}
