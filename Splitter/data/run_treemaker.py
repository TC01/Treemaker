#!/usr/bin/env python

# Minimally modified version of one of Marc's treemaking scripts.
# Has (human intelligible) command line opts.

import os
import glob
import sys
from DataFormats.FWLite import Events, Handle
import ROOT

from Type1Trees import *
from Type2Trees import *

from optparse import OptionParser

def runTreemaker(files, n, mc, weight, PUfiles):
	events = Events(files)
	ntotal = events.size()

	ana1 = Type1treemaker(n, mc, weight, PUfiles)
	ana2 = Type2treemaker(n, mc, weight, PUfiles)
	
	count = 0
	print "Start looping"
	for event in events:
		count = count + 1
		if count % 5000 == 0 or count == 1:
	      		percentDone = float(count) / float(ntotal) * 100.0
	       		print 'Processing {0:10.0f}/{1:10.0f} : {2:5.2f} %'.format(count, ntotal, percentDone )
		e1 = ana1.analyze(event)
		e2 = ana2.analyze(event)
	del ana1
	del ana2


if __name__ == '__main__':
	parser = OptionParser()

	parser.add_option('-n', '--name', metavar='NAME', type='string', dest='n', help="The name of the output file, minus the .root.")
	parser.add_option('-f', '--files', metavar='FILES', type='string', dest='files', help="Location of the ntuples to run over.")
	parser.add_option('-p', '--PUfiles', metavar='FILES', type='string', dest='PUfiles', help="Location of the PU file")
	parser.add_option('-m', '--isMC', metavar='FILES', action='store_true', default=False, dest='mc', help="set MC vars?")
	parser.add_option('-w', '--weight', metavar='FILES', type='float', default=1.0, dest='weight', help="event weight")

	(options, args) = parser.parse_args()

	#FILES = os.path.join(options.files, "*.root")
	# ...
	FILES = options.files + "*.root"
	files = glob.glob(FILES)
	print files

	runTreemaker(files, options.n, options.mc, options.weight, options.PUfiles)
