let
  pythonPackageOverlay = overlay: attr: final: prev: {
    ${attr} = final.lib.fix (py:
      prev.${attr}.override (old: {
        self = py;
        packageOverrides = final.lib.composeExtensions
          (old.packageOverrides or (_: _: { }))
          overlay;
      }));
  };
in
pythonPackageOverlay
  (final: prev: {
    pyTuplingUtils = prev.callPackage ./default.nix { };
  }) "python3"
