{
  description = "pyfeed: a simple cli rss feed reader";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-23.05";
  };

  outputs = { self, nixpkgs } @ inputs:
    let
      pkgs = nixpkgs.legacyPackages.x86_64-linux;
    in
    {
      devShells.x86_64-linux.default = pkgs.mkShell {
          packages = with pkgs; [
            python311
            python311Packages.requests
            python311Packages.prettytable
            python311Packages.python-lsp-server
            python311Packages.beautifulsoup4
            python311Packages.lxml
          ];
        };
    };
}
