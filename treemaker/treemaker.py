#!/usr/bin/env python

import multiprocessing
import optparse
import os
import sys

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from DataFormats.FWLite import Events, Handle

def runTreemaker(directory, name=""):
	print "*** Running treemaker over " + directory
	if name == "":
		name = directory.rpartition("/")[2]
	if not ".root" in name:
		name += ".root"
	print "*** Output file name = " + name

def main():
	parser = optparse.OptionParser()

	(opts, args) = parser.parse_args()

	for arg in args:
		directory = os.path.abspath(arg)
		if not os.path.exists(directory):
			print "Error: no such directory: " + arg
			sys.exit(1)
		runTreemaker(directory)

if __name__ == '__main__':
	main()
