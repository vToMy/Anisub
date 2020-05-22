import sys
from pathlib import Path

from PyInstaller.__main__ import run

from anisub import __main__

if __name__ == '__main__':

    spec_path = Path(__main__.__file__).with_suffix('.spec').name
    sys.argv.append(spec_path)
    sys.argv.append('-y')   # remove output directory without confirmation
    run()
