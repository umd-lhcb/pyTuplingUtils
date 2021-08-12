{ stdenv, buildPythonPackage, fetchPypi, matplotlib, numpy, packaging, uhi }:

buildPythonPackage rec {
  pname = "mplhep";
  version = "0.3.10";

  src = fetchPypi {
    inherit pname version;
    sha256 = "37d39f42c15e15bca72ea0f7674212cb57e8a48b028d3202f242d6525cc1704f";
  };

  patches = [
    ./no_font_from_mplhep_data.patch
  ];

  propagatedBuildInputs = [ matplotlib numpy packaging uhi ];

  doCheck = false;
}
