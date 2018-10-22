#!/usr/bin/env python

import sys

import make_c





def main():
    print sys.argv
    argv=sys.argv[1:]
    make_c.main(argv)
    

