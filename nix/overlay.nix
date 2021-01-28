let
  pythonPackageOverlay = overlay: attr: self: super: {
    ${attr} = self.lib.fix (py:
      super.${attr}.override (old: {
        self = py;
        packageOverrides = self.lib.composeExtensions
          (old.packageOverrides or (_: _: { }))
          overlay;
      }));
  };
in
pythonPackageOverlay
  (self: super: {
    pyTuplingUtils = super.callPackage ./default.nix { };
  }) "python3"
