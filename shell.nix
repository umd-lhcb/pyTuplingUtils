with import <nixpkgs> {};

let
  python = enableDebugging pkgs.python3;
  pythonPackages = python.pkgs;
in

pkgs.mkShell {
  name = "pip-env";
  buildInputs = with pythonPackages; [
    # Compilers and other build dependencies
    pkgs.stdenv

    # Auto completion
    jedi

    # Linters
    flake8
    pylint

    # Python requirements (enough to get a virtualenv going).
    virtualenvwrapper
  ];

  shellHook = ''
    # Allow the use of wheels.
    SOURCE_DATE_EPOCH=$(date +%s)

    if test -d $HOME/build/python-venv; then
      VENV=$HOME/build/python-venv/pyTuplingUtil
    else
      VENV=./.virtualenv
    fi

    if test ! -d $VENV; then
      virtualenv $VENV
    fi
    source $VENV/bin/activate

    # allow for the environment to pick up packages installed with virtualenv
    export PYTHONPATH=$VENV/${python.sitePackages}/:$PYTHONPATH
  '';
}
