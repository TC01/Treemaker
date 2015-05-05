# Pruner for trees. Takes a tree and removes events not passing certain cuts.

# Code written by Marc. Memo to add some error checking to it someday. --Ben

import os
import ROOT
from ROOT import *
import sys

from optparse import OptionParser
parser = OptionParser()
parser.add_option('--n', metavar='N', type='string', action='store',
                  dest='nm',
                  help='')
parser.add_option('--o', metavar='O', type='string', action='store',
                  dest='out',
                  help='')
parser.add_option('--t', metavar='T', type='string', action='store',
                  dest='tree',
                  help='')
parser.add_option('--c', metavar='C', type='string', action='store',
                  dest='CUTS',
                  help='')
(options, args) = parser.parse_args()

f = TFile(options.nm)
t = f.Get(options.tree)

newf = TFile("holding.root", "recreate" )
newf.cd()

T = t.CopyTree(options.CUTS)
T.SetName(options.tree)

newnewf = TFile(options.out+".root", "recreate")
newnewf.cd()

TT = T.CopyTree('')
TT.SetName(options.tree)

newnewf.Write()
newnewf.Save()
