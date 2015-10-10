#!/usr/bin/env python

import copy
import sys
import subprocess

# Script to run the real command-- treepruner.
# The tree pruning code *could* go into a module but this might be better.

if __name__ == '__main__':
	arguments = copy.copy(sys.argv)
	arguments[0] = arguments[0].replace('TreePruner.py', 'treepruner')
	subprocess.call(arguments)