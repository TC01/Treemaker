# SingleElectron_2015C configuration

#import os
#import sys

#sys.path.append(os.getcwd())

import run_treemaker

# File location.
location = "/eos/uscms/store/user/bjr/76X/data/SingleElectron_2016C/"

# Configuration parameters that run() uses, globals, hardcoded.
name_root = "SingleElectron_Run2015C"
mc = False
weight = 1.0
pileups = "/uscms_data/d3/bjr/frameworks/CMSSW_7_6_3_patch2/src/Treemaker/Splitter/data/marc-treemaker/PU_weights_test.root"

# The function to be passed a list of files and actually do things.
def run(files, name_append=""):
	name = name_root + name_append
	run_treemaker.runTreemaker(files, name, mc, weight, pileups)

# The location of the files.
# Anything Treemaker knows how to understand is acceptable here.
def getFiles():
	return location

def getName():
	return name_root
