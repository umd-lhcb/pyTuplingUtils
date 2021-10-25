# NOTE: Older versions of nix have a problem regarding the 'follows' sematics.
#       Don't use this flake inside another flake that will used by a third flake!
{
  description = "Utilities for ntuples, such as plotting and simple debugging";

  inputs = {
    root-curated.url = "github:umd-lhcb/root-curated";
    nixpkgs.follows = "root-curated/nixpkgs";
    flake-utils.follows = "root-curated/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils, root-curated }:
    {
      overlay = import ./nix/overlay.nix;
    }
    //
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
          overlays = [ self.overlay root-curated.overlay ];
        };
        python = pkgs.python3;
        pythonPackages = python.pkgs;
      in
      {
        packages = flake-utils.lib.flattenTree {
          pyTuplingUtilsDev = pythonPackages.pyTuplingUtils;
        };

        devShell = pkgs.mkShell rec {
          name = "pyTuplingUtils-dev";
          buildInputs = with pythonPackages; [
            # Dev tools
            jedi
            flake8
            pylint
            virtualenvwrapper

            # Pinned Python dependencies
            numpy
          ];

          shellHook = ''
            # Allow the use of wheels.
            SOURCE_DATE_EPOCH=$(date +%s)

            if test -d $HOME/build/python-venv; then
              VENV=$HOME/build/python-venv/${name}
            else
              VENV=./.virtualenv
            fi

            if test ! -d $VENV; then
              virtualenv $VENV
            fi
            source $VENV/bin/activate

            # allow for the environment to pick up packages installed with virtualenv
            export PYTHONPATH=$VENV/${python.sitePackages}/:$PYTHONPATH

            # fix libstdc++.so not found error
            export LD_LIBRARY_PATH=${pkgs.stdenv.cc.cc.lib}/lib:$LD_LIBRARY_PATH
          '';
        };
      });
}
