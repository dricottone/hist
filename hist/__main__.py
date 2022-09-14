#!/usr/bin/env python

import sys
import fileinput

from . import cli
from . import histogram

def main():
    _config, _positionals = cli.main(sys.argv[1:])

    if "version" in _config.keys():
        sys.exit(0)
    elif "help" in _config.keys():
        sys.exit(0)

    _bins = int(_config.get("bins", 10))
    _positive = "positive" in _config.keys()

    data = []
    with fileinput.input(files=_positionals, encoding="utf-8") as f:
        data.extend([float(line.rstrip()) for line in f])

    histogram.draw(data, _bins, _positive)


if __name__ == '__main__':
    main()

