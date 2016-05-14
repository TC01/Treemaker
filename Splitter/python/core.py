# Splitter core.
# Splitter is a much-slimmed-down Treemaker that uses the same splitting logic.

import os
import multiprocessing
import sys

from Treemaker.Treemaker import core as tmcore
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

def split(jobfile, splitInto, splitBy, index=-1):

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
	try:
		job, splitNtuples, numJobs = split(jobfile, splitInto, splitBy, index)
		runstring = ""
		if index != -1:
			runstring = "Index" + str(index)
		job.run(splitNtuples, runstring)
	except KeyboardInterrupt:
		raise tmcore.KeyboardInterruptError()

def runMultiJob(jobfile, splitInto, splitBy, startAt=0):
	job, splitNtuples, numJobs = split(jobfile, splitInto, splitBy)

	# Make the jobs via multiprocessing!
	pool = multiprocessing.Pool()
	results = []
	# Start at wherever we're told to start at.
	for index in range(startAt, numJobs):
		result = pool.apply_async(runSplitJob, (jobfile, splitInto, splitBy, index, ))
		results.append(result)

	pool.close()
	pool.join()
	for result in results:
		result.get(timeout=tmcore.treemakerTimeout)
