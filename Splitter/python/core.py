# Splitter core.
# Splitter is a much-slimmed-down Treemaker that uses the same splitting logic.

import os
import sys

from Treemaker.Treemaker import filelist

def readConfig(jobfile):
	# This is a silly hack and makes me sad.
	# Import the (Python) configuration
	if not os.path.exists(jobfile):
		print "Error: invalid job file specified!"
		return
	path, _, filename = jobfile.rpartition("/")
	module = filename.split(".")[0]
	sys.path.append(os.path.abspath(path))
	job = __import__(module)

	# Return the configuration object.
	return job

def split(jobfile, splitInto, splitBy, index):

	# Read parameters from the configuraiton.
	job = readConfig(jobfile)
	location = job.getFiles()
	name = job.getName()
	
	# Get the list of ntuples.
	ntuples, name = filelist.getNtuplesAndName(location, name)

	# Do job splitting, figure out what we want.
	splitNtuples, numJobs = filelist.doSplitting(ntuples, index, splitBy, splitInto)

	# Return the job, the ntuples, and the number of jobs total.
	return job, splitNtuples, numJobs

def runSplitJob(jobfile, splitInto, splitBy, index):
	job, splitNtuples, numJobs = split(jobfile, splitInto, splitBy, index)
	runstring = "Index" + str(index)
	job.run(splitNtuples, runstring)
