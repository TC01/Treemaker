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

def doSplitting(ntuples, index, splitBy, splitInto):
	"""	Do job splitting. Given splitting options, a list of files (strings) and an index,
		splits the files and returns the (index)th set of files to process. Also returns
		the total number of jobs needed."""
	numNtuples = len(ntuples)
	# These cases should be mutually exclusive.
	if splitBy > 0:
		numJobs = splitBy
		startJobs = int(math.ceil(numNtuples / float(splitBy))) * index
		endJobs = int(math.ceil(numNtuples / float(splitBy))) * (index + 1)
		if index + 1 > splitBy:
			print "Error: cannot make this splitting with index + 1 > number of splits!"
			sys.exit(1)
	elif splitInto > 0:
		startJobs = splitInto * index
		endJobs = splitInto * (index + 1)
		numJobs = int(math.ceil(len(ntuples) / float(splitInto)))

	if (splitBy > 0 or splitInto > 0) and index >= 0:
		if endJobs > len(ntuples):
			endJobs = len(ntuples)
		return ntuples[startJobs:endJobs], numJobs
	else:
		return ntuples, numJobs

def getNtuplesAndName(directory):
	if 'dbs://' in directory or 'dbs://' in directory:
		# For DAS entries, look them up using dbsapi (or the bit of it we wrote).
		ntuples, dataset = filelist.getDASNtuples(directory)

		print "*** Running treemaker over dataset " + dataset
		if name == "":
			name = dataset.split('/')[1]
	else:
		print "*** Running treemaker over " + directory
		if name == "":
			name = directory.rpartition("/")[2]
		ntuples = filelist.getDiskNtuples(directory)