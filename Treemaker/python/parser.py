"""
Command-line parser, now that that is shared between scripts.
"""

import config

def getParser():
	parser = optparse.OptionParser()
	parser.add_option("-c", "--config", dest="config", help="The name of the config file containing all plugin names. This option is required.", default="")
	parser.add_option("-d", "--data", dest="data", action="store_true", help="If true, we are running on data.")
	parser.add_option("-f", "--force", dest="force", action="store_true", help="If true, delete things and overwrite things.")
	parser.add_option("-l", "--linear", dest="linear", action="store_true", help="If true, disable multiprocessing.")
	parser.add_option("-n", "--name", dest="name", help="The name of the output file, defaults to directory name of ntuples.", default="")
	parser.add_option("-t", "--treename", dest="treename", help="The name of the output TTree object.", default="tree-" + version)
	
	parser.add_option('--split-into', dest='splitInto', help="Maximum number of jobs to run in each split.", default=None)
	parser.add_option('--split-by', dest='splitBy', help="Number of splits to make.", default=None)
	
	return parser

def getCLIParser():
	parser = getParser()

	parser.add_option('--split-index', dest='splitIndex', help="The nth split to run, using the job-split parameters.", default=None)
	
	return parser
	
def getCondorParser():
	# TODO: add condor params.
	
	parser = getParser()
	
	return parser