"""
Command-line parser, now that that is shared between scripts.
"""

# Used so trees from multiple versions do not get hadd'd together.
version = "0.3"

def getParser():
	parser = optparse.OptionParser()
	parser.add_option("-c", "--config", dest="config", help="The name of the config file containing all plugin names. This option is required.", default="")
	parser.add_option("-d", "--data", dest="data", action="store_true", help="If true, we are running on data.")
	parser.add_option("-f", "--force", dest="force", action="store_true", help="If true, delete things and overwrite things.")
	parser.add_option("-l", "--linear", dest="linear", action="store_true", help="If true, disable multiprocessing.")
	parser.add_option("-n", "--name", dest="name", help="The name of the output file, defaults to directory name of ntuples.", default="")
	parser.add_option("-t", "--treename", dest="treename", help="The name of the output TTree object.", default="tree-" + version)
	return parser

def getCLIParser():
	parser = getParser()
	# TODO: add job-splitting params.
	return parser
	
def getCondorParser():
	# TODO: add condor params.
	return getParser()