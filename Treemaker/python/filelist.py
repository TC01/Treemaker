"""
Routines to get the list of files to run over.
"""

import os
import sys

from Treemaker.Treemaker.dbsapi import dasFileQuery
from Treemaker.Treemaker.dbsapi import constants

def getDASNtuples(directory):
	"""	Given a das 'url', extract the list of files to run over.
		Returns a list of ntuples in xrootd form and the dataset name."""
	_, _, dasName = directory.partition("://")
	dbs, _, dataset = dasName.partition(":")
	if not dbs in constants.instances:
		print "Error: DBS instance " + dbs + " was not recognized!"
		sys.exit(1)
	rawNtuples = dasFileQuery.dasFileQuery(dataset, dbs)
	ntuples = ["root://cmsxrootd.fnal.gov//" + ntuple for ntuple in rawNtuples]
	return ntuples, dataset

def getDiskNtuples(directory):
	"""	Given a directory on a proper filesystem, return a list of ntuples to run over."""
		# Accumulate a list of files. Subdirectories are okay.
	ntuples = []
	for path, dirs, files in os.walk(directory):
		for ntuple in files:
			if '.root' in ntuple:
				ntuples.append(os.path.join(path, ntuple))
	return ntuples