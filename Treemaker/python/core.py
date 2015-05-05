"""
The core of Treemaker, implemented inside the library.
"""

# Python standard library.
import array
import multiprocessing
import optparse
import os
import shutil
import sys

# ROOT and FWLite dependencies.
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from DataFormats.FWLite import Events, Handle

# Other.
import numpy

# Our own libraries.
from Treemaker.Treemaker import labels
from Treemaker.Treemaker import plugins

def loadPlugins(config):
	pluginNames = []
	try:
		if config == "":
			raise RuntimeError
		with open(config) as configFile:
			for line in configFile:
				line = line.rstrip('\n')
				if not line.lstrip().rstrip() == "" and not line[0] == "#":
					pluginNames.append(line)
	except RuntimeError:
		print "ERROR: attempted to run Treemaker without specifying plugins!"
		print "The safest thing to do is fail."
		print "Please rerun Treemaker with the -c [config name] option, where [config name]"
		print "is a file containing newline-separated list of plugin names."
		sys.exit(1)
	
	# Actually load the plugins.
	plugins.loadPlugins(pluginNames)

def runOverNtuple(ntuple, outputDir, treename, data=False):
	print "**** Processing ntuple: " + ntuple
	outputName = os.path.join(outputDir, ntuple.rpartition("/")[2])
	output = ROOT.TFile(outputName, "RECREATE")
	tree = ROOT.TTree(treename, treename)

	# Create the label dictionary.
	labelDict = labels.getLabels(ntuple)
	
	# Set up branches for all variables declared by loaded plugins.
	variables = {}
	variables = plugins.setupPlugins(variables, data)
	for varName, varArray in variables.iteritems():
		tree.Branch(varName, varArray, varName + '/F')

	# Create the cuts array.
	cuts = {}
	cuts = plugins.createCutsPlugins(cuts)
	# For reasons that I'm sure I'd rather not know, this does not work.
	# Despite the fact that I lifted this line from writeEvents, my old
	# treemaker/converter I wrote back in 2013... I hate everything.
#	cutArray = numpy.zeros(len(cuts))
	cutArray = array.array('i', [0] * len(cuts))
	tree.Branch("cuts", cutArray, "cuts[" + str(len(cuts)) + "]/I")
	# We care about order here so it's consistent.
	ordered = sorted(cuts, key=cuts.get)
	for i in xrange(len(ordered)):
		name = ordered[i]
		cuts[name].index = i
		
	# Now, run over all events.
	for event in Events(ntuple):
		labelDict = labels.fillLabels(event, labelDict)
		variables = plugins.analyzePlugins(event, variables, labelDict, data)

		cuts = plugins.makeCutsPlugins(event, variables, cuts, labelDict, data)
		for name, cut in cuts.iteritems():
			cutArray[cut.index] = cut.passed

		tree.Fill()
		variables = plugins.resetPlugins(variables)
		for name, cut in cuts.iteritems():
			cutArray[cut.index] = 0

	output.cd()
	tree.Write()
	output.Write()
	output.Close()
	print "**** Finished processing ntuple " + ntuple

def doSplitting(ntuples, index, splitBy, splitInto):
	numNtuples = len(ntuples)
	# These cases should be mutually exclusive.
	if splitBy > 0:
		startJobs = (numNtuples / splitBy) * index
		endJobs = (numNtuples / splitBy) * (index + 1) - 1
		if index + 1 > splitBy:
			print "Error: cannot make this splitting with index + 1 > number of splits!"
			sys.exit(1)
	elif splitInto > 0:
		startJobs = splitInto * index
		endJobs = splitInto * (index + 1) - 1

	if splitBy > 0 or splitInto > 0:
		if endJobs >= len(ntuples):
			endJobs = len(ntuple) - 1
		return ntuples[startJobs:endJobs]
	else:
		return ntuples

#def runTreemaker(directory, treename="tree", data=False, force=False, name="", linear=False):
def runTreemaker(treemakerConfig):
	
	# Read arguments from config and load plugins.
	directory = treemakerConfig.directory
	name = treemakerConfig.fileName
	data = treemakerConfig.isData
	linear = treemakerConfig.linear
	force = treemakerConfig.force
	treename = treemakerConfig.treeName
	index = treemakerConfig.splitIndex
	plugins.loadPlugins(treemakerConfig.pluginNames)

	# Create output name
	print "*** Running treemaker over " + directory
	if name == "":
		name = directory.rpartition("/")[2]
	if not ".root" in name:
		name += ".root"
	if index != -1:
		name = "Index" + str(index) + "_" + name
	print "*** Output file name = " + name

	outputDir = os.path.join(os.getcwd(), name + "_temp")
	try:
		os.mkdir(outputDir)
	except OSError:
		print "Error: unable to create temporary output directory."
		if force:
			print "Removing directory that was there and proceeding..."
			shutil.rmtree(outputDir)
			os.mkdir(outputDir)
		else:
			print "Please deal with the directory " + outputDir
			print "Or run treemaker -f."
			return

	pool = multiprocessing.Pool()
	results = []
	
	# Accumulate a list of files. NO SUBDIRECTORIES, I may change my mind on this one
	# once I consider how the sorting should happen.
	ntuples = []
	for path, dirs, files in os.walk(directory):
		if path == directory:
			for ntuple in files:
				ntuples.append(ntuple)

	# Do splitting.
	ntuples = sorted(ntuples)
	splitNtuples = doSplitting(ntuples, index, treemakerConfig.splitBy, treemakerConfig.splitInto)

	for ntuple in splitNtuples:
		workingNtuple = os.path.join(path, ntuple)
		if linear:
			runOverNtuple(workingNtuple, outputDir, treename)
		else:
			result = pool.apply_async(runOverNtuple, (workingNtuple, outputDir, treename, data, ))
			results.append(result)

	pool.close()
	pool.join()

	# For now use os.system to run hadd, we should figure out a better way.
	# But this works, so...
	haddCommand = "hadd "
	if force:
		haddCommand += " -f "
	os.system(haddCommand + name + " " + outputDir + "/*")

	# We can rely on the ordering here to make things be the same order
	# as they were in the subprocesses, to generate a report.
	cuts = {}
	cuts = plugins.createCutsPlugins(cuts)	
	ordered = sorted(cuts, key=cuts.get)
	for i in xrange(len(ordered)):
		cutName = ordered[i]
		cuts[cutName].index = i

	# Generate output cuts report.
	# TODO: store inside the tree itself.
	reportName = name.partition(".")[0] + "_cuts_report.txt"
	with open(reportName, 'wb') as report:
		for cutName, cut in cuts.iteritems():
			report.write(str(cut) + "\n")

	shutil.rmtree(outputDir)
