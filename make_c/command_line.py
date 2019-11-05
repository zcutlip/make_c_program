#!/usr/bin/env python3

import sys
from make_c import make_c


def main():
    argv = sys.argv[1:]
    make_c.main(argv)
