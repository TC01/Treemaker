#!/usr/bin/env python

import multiprocessing
import optparse
import os
import shutil
import sys

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from DataFormats.FWLite import Events, Handle

def runOverNtuple(ntuple, output):
	for event in Events(ntuple):
		

def runTreemaker(directory, name=""):
	print "*** Running treemaker over " + directory
	if name == "":
		name = directory.rpartition("/")[2]
	if not ".root" in name:
		name += ".root"
	print "*** Output file name = " + name

	outputDir = os.path.join(os.getcwd(), name + "_temp")
	try:
		os.mkdir(outputDir)
	except OSError:
		print "Error: unable to create temporary output directory."
		print "Please deal with the directory " + outputDir
		return

	pool = multiprocessing.Pool()

	for path, dirs, files in os.walk(directory):
		if path == directory:
			for ntuple in files:
				pool.apply_async(runOverNtuple, (os.path.join(path, ntuple), outputDir,))

	pool.join()
	# For now use os.system:
	os.system("hadd " + name + " " + outputDir + "/*")

	shutil.rmtree(outputDir)

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
