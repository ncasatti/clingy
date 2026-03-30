{
  description = "Context-aware CLI framework with fuzzy search menus and auto-discovery";

  # --- INPUTS ---
  # Define where we fetch our packages from.
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  # --- OUTPUTS ---
  # This function defines what this flake provides to the outside world.
  outputs = {
    self,
    nixpkgs,
  }: let
    # We define the architecture.
    system = "x86_64-linux";
    pkgs = nixpkgs.legacyPackages.${system};

    python = pkgs.python311;
  in {
    # --- THE COMPILED PACKAGE ---
    packages.${system}.default = python.pkgs.buildPythonApplication {
      pname = "clingy";
      version = "1.1.0";

      # Parse and use the pyproject.toml standard.
      pyproject = true;

      # The source code is the current directory.
      src = ./.;

      # Build System: What compiles the code.
      build-system = [
        python.pkgs.setuptools
      ];

      # Runtime Dependencies: Packages required for clingy to run
      dependencies = [
        python.pkgs.pyyaml
      ];

      # Binary Wrapping
      # Inject 'fzf' directly into the runtime PATH of the compiled Clingy binary.
      makeWrapperArgs = [
        "--prefix PATH : ${pkgs.lib.makeBinPath [pkgs.fzf]}"
      ];
    };

    # --- THE DEVELOPMENT ENVIRONMENT ---
    # Activated when run 'nix develop' or use 'direnv'.
    devShells.${system}.default = pkgs.mkShell {
      # Tools available while developing the framework.
      buildInputs = [
        python
        pkgs.uv
        pkgs.fzf

        # Formatters and linters from your dev dependencies
        pkgs.black
        pkgs.mypy
        pkgs.isort
      ];

      # Welcome message
      shellHook = ''
        echo "========================================"
        echo " Clingy Dev Environment Active"
        echo " Python, uv, and fzf are ready to use."
        echo "========================================"
      '';
    };
  };
}
