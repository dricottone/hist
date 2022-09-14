#!/usr/bin/env python

VERSION=(1,0,0,)

import sys
import fileinput

from . import cli
from . import histogram

def main():
    _config, _positionals = cli.main(sys.argv[1:])

    if "version" in _config.keys():
        sys.stderr.write(f"hist {'.'.join(str(v) for v in VERSION)}\n")
        sys.exit(0)
    elif "help" in _config.keys():
        sys.stderr.write(f"Usage: hist [OPTIONS]\n")
        sys.stderr.write(f"Options:\n")
        sys.stderr.write(f"  -b=BINS, --bins=BINS  number of bins in histogram [Default: 10]\n")
        sys.stderr.write(f"  -h, -x, --help        print this message and exit\n")
        sys.stderr.write(f"  -p, --positive        force scale to be positive\n")
        sys.stderr.write(f"  -v, -V, --version     print version and exit\n")
        sys.exit(0)

    _bins = int(_config.get("bins", 10))
    _positive = "positive" in _config.keys()

    data = []
    with fileinput.input(files=_positionals, encoding="utf-8") as f:
        data.extend([float(line.rstrip()) for line in f])

    histogram.draw(data, _bins, _positive)


if __name__ == '__main__':
    main()

