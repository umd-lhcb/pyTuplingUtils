{ stdenv, buildPythonPackage, fetchPypi, numpy }:

buildPythonPackage rec {
  pname = "uhi";
  version = "0.3.0";

  src = fetchPypi {
    inherit pname version;
    sha256 = "3f441bfa89fae11aa762ae1ef1b1b454362d228e9084477773ffb82d6e9f5d2c";
  };

  propagatedBuildInputs = [ numpy ];

  doCheck = false;
}
