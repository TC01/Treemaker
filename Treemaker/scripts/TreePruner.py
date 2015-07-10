#!/usr/bin/env python

# Pruner for trees. Takes a tree and removes events not passing certain cuts.

# Code originally written by Marc, modified by Ben to have a better CLI
# more in line with what the other treemaker commands do.

# Code written by Marc, modified by Ben to be more forgiving and have better
# command line options (with help text and defaults).

import os
import ROOT
import sys

from optparse import OptionParser
parser = OptionParser()
parser.add_option('-n', '--name', dest='name', help="Input filename.")
parser.add_option('-o', '--out', dest='out', default="", help='Output name, defaults to input name with _pruned appended.')
parser.add_option('-t', '--tree', dest='tree', default='tree', help='Tree name, defaults to tree.')
parser.add_option('-c', '--cuts', dest='cuts', default="", help='The cut to apply to the selection')
(options, args) = parser.parse_args()

inputName = options.name
if not '.root' in options.name:
	inputName += '.root'

# Some error checking, as promised.
try:
	f = ROOT.TFile(inputName)
except:
	print "Error: invalid root file " + inputName
	sys.exit(1)

t = f.Get(options.tree)

newf = ROOT.TFile("holding.root", "recreate" )
newf.cd()

try:
	T = t.CopyTree(options.cuts)
	T.SetName(options.tree)
except:
	print "Error: unable to copy tree, please check the tree name '" + options.tree + "', or the cuts string '" + options.cuts + "'"
	sys.exit(1)

# Default output name.
out = options.out
if out == '':
	out = inputName.split('.')[0] + '_pruned.root'

newnewf = ROOT.TFile(out, "recreate")
newnewf.cd()

TT = T.CopyTree('')
TT.SetName(options.tree)

newnewf.Write()
newnewf.Save()

# Clean up the holding.root file.
os.remove("holding.root")
