"""
Command-line parser, now that that is shared between scripts.
"""

import optparse

from Treemaker.Treemaker import config

def getParser():
	parser = optparse.OptionParser()
	parser.add_option("-f", "--force", dest="force", action="store_true", help="If true, delete things and overwrite things.")
	parser.add_option("-l", "--linear", dest="linear", action="store_true", help="If true, disable multiprocessing.")

	# These options should maybe go away.
	parser.add_option("-d", "--data", dest="data", action="store_true", help="If true, we are running on data.", default=False)
	parser.add_option("-n", "--name", dest="name", help="The name of the output file, defaults to directory name of ntuples.", default=config.defaultFileName)
	parser.add_option("-t", "--treename", dest="treename", help="The name of the output TTree object.", default=config.defaultTreeName)
	
	parser.add_option('--split-into', dest='splitInto', help="Maximum number of jobs to run in each split.", default=-1, type=int)
	parser.add_option('--split-by', dest='splitBy', help="Number of splits to make.", default=-1, type=int)
	
	return parser

def getCLIParser():
	parser = getParser()

	parser.add_option('--split-index', dest='splitIndex', help="The nth split to run, using the job-split parameters.", default=-1, type=int)
	
	return parser
	
def getCondorParser():
	parser = getParser()
	parser.add_option("-r", "--run", dest="run", action="store_true", default=False, help="Whether or not to run the condor job after creating it.")	
	return parser

def getConfigParser():
	parser = getParser()
	parser.add_option("-p", "--plugin-list", dest="pluginList", help="Newline-separated list of plugins to add to generated config file.", default="")
	parser.add_option("-o", "--output-name", dest="outputName", help="Name of output file, defaults to name of dataset.", default="")
	return parser
