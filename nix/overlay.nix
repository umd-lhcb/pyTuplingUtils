final: prev:

{
  pythonOverrides = prev.lib.composeExtensions prev.pythonOverrides (finalPy: prevPy: {
    pyTuplingUtils = finalPy.callPackage ./default.nix { };
  });
  python3 = prev.python3.override { packageOverrides = final.pythonOverrides; };
}
