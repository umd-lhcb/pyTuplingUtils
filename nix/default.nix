{ stdenv
, buildPythonPackage
, uproot
, lz4
, numpy
, matplotlib
, lark-parser
, tabulate
}:

buildPythonPackage rec {
  pname = "pyTuplingUtils";
  version = "0.2.6.2";

  src = builtins.path { path = ./..; name = pname; };

  buildInputs = [ root ];
  propagatedBuildInputs = [
    uproot
    lz4
    numpy
    matplotlib
    lark-parser
    tabulate
  ];

  doCheck = false;
}
