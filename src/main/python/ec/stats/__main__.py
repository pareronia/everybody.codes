#! /usr/bin/env python3

import logging
import sys

from .stats import main

logging.basicConfig(level=logging.INFO)
args = sys.argv[1:]
if "-v" in args:
    logging.getLogger("ec.stats").setLevel(logging.DEBUG)
if "-vv" in args:
    logging.getLogger().setLevel(logging.DEBUG)
    args = [a for a in args if a != "-vv"]
main(args)
