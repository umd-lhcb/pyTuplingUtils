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
          overlays = [ root-curated.overlay self.overlay ];
        };
        python = pkgs.python3;
        pythonPackages = python.pkgs;
      in
      {
        packages = flake-utils.lib.flattenTree {
          pyTuplingUtils = python.withPackages (p: with p; [ pyTuplingUtils ]);
        };

        devShell = pkgs.mkShell rec {
          name = "pyTuplingUtils-dev";
          buildInputs = with pythonPackages; [
            # Dev tools
            pylint
            # Pinned Python dependencies
            pythonPackages.pyTuplingUtils
          ];
        };
      });
}
