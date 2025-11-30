# Replit Nix Configuration for FinRobot
# Provides system-level dependencies for the Python environment

{ pkgs }: {
  deps = [
    # Python 3.11
    pkgs.python311
    
    # Python package managers
    pkgs.python311Packages.pip
    pkgs.python311Packages.setuptools
    pkgs.python311Packages.wheel
    
    # System libraries
    pkgs.glibcLocales
    
    # Build tools
    pkgs.git
    pkgs.curl
    pkgs.wget
    
    # Additional utilities
    pkgs.bash
    pkgs.coreutils
  ];
  
  env = {
    # Python binary path
    PYTHONBIN = "${pkgs.python311}/bin/python3.11";
    
    # Locale settings
    LANG = "en_US.UTF-8";
    LC_ALL = "en_US.UTF-8";
    
    # Python path
    PYTHONPATH = "${pkgs.python311}/lib/python3.11/site-packages";
  };
}
