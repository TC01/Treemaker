"""
The core of Treemaker, implemented inside the library.
"""

# Python standard library.
import array
import math
import multiprocessing
import optparse
import os
import shutil
import sys

# ROOT and FWLite dependencies.
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from DataFormats.FWLite import Events, Handle

# Our own libraries.
from Treemaker.Treemaker import constants
from Treemaker.Treemaker import cuts
from Treemaker.Treemaker import filelist
from Treemaker.Treemaker import labels
from Treemaker.Treemaker import leaves
from Treemaker.Treemaker import plugins

# Perhaps this should be configurable, but a 'timeout' for the treemaker.
# If your jobs take longer than 12 hours to run, please make use of the
# splitting commands. :)
treemakerTimeout = 43200	# (60 * 60 * 12) seconds

# Courtesy of StackOverflow.
# https://stackoverflow.com/questions/1408356/keyboard-interrupts-with-pythons-multiprocessing-pool
class KeyboardInterruptError(Exception): pass

def runOverTree(inputTree, tree, runner, labelDict, variables, cutDict, cutArray, data):
	"""	Run over a ttree, not a ntuple."""
	numEntries = inputTree.GetEntries()
	for i in range(numEntries):
		labelDict = leaves.fillLeaves(inputTree, labelDict, i)

		variables, cutDict, shouldDrop = runner.analyzePlugins(inputTree, variables, cutDict, labelDict, data)
		for name, cut in cutDict.iteritems():
			cutArray[cut.index] = cut.passed

		# Check if any plugin says that we should drop the event.
		# If the event is being dropped, simply don't call Fill()
		if not shouldDrop:
			tree.Fill()

		# Reset our variables and cuts dictionaries.
		variables = runner.resetPlugins(variables)
		for name, cut in cutDict.iteritems():
			cutArray[cut.index] = 0
			cut.passed = 0

def runOverNtuple(ntuple, tree, runner, labelDict, variables, cutDict, cutArray, data):
	# Now, run over all events.
	for event in Events(ntuple):
		labelDict = labels.fillLabels(event, labelDict)

		variables, cutDict, shouldDrop = runner.analyzePlugins(event, variables, cutDict, labelDict, data)
		for name, cut in cutDict.iteritems():
			cutArray[cut.index] = cut.passed

		# Check if any plugin says that we should drop the event.
		# If the event is being dropped, simply don't call Fill()
		if not shouldDrop:
			tree.Fill()

		# Reset our variables and cuts dictionaries.
		variables = runner.resetPlugins(variables)
		for name, cut in cutDict.iteritems():
			cutArray[cut.index] = 0
			cut.passed = 0

def runOverFile(treemakerConfig, ntuple, outputDir, treename, offset, data=False):
	
	# Load input type from configuration object.
	inputType = treemakerConfig.inputType
	
	# Large try/except block.
	try:
		
		# Load plugins, silently, turn them into a class.
		pluginArray = plugins.loadPlugins(treemakerConfig.pluginNames, treemakerConfig.configVars, True, inputType)
		runner = plugins.PluginRunner(pluginArray)

		print "**** Processing file: " + ntuple
		outputName = os.path.join(outputDir, str(offset) + "_" + ntuple.rpartition("/")[2])
		output = ROOT.TFile(outputName, "RECREATE")
		tree = ROOT.TTree(treename, treename)

		# Create the label/leaf dictionary.
		if inputType == "Ntuple":
			labelDict = labels.getLabels(ntuple)
		elif inputType == "Tree":
			labelDict = leaves.getLeaves(ntuple)

		# Set up branches for all variables declared by loaded plugins.
		# Do this setup in sorted alphabetical order by variable name.
		variables = runner.setupPlugins({}, data)
		sortedVarNames = sorted(variables)
		for varName in sortedVarNames:
			varArray = variables[varName]
			tree.Branch(varName, varArray, varName + '/F')

		# Create the cuts array.
		cutDict = {}
		cutDict = runner.createCutsPlugins(cutDict)
		cutArray = array.array('i', [0] * len(cutDict))
		tree.Branch("cuts", cutArray, "cuts[" + str(len(cutDict)) + "]/I")
		# We care about order here so it's consistent.
		ordered = sorted(cutDict)
		for i in xrange(len(ordered)):
			name = ordered[i]
			cutDict[name].index = i

		# Run over the actual file, depending on what type of file it is!
		if inputType == "Ntuple":
			runOverNtuple(ntuple, tree, runner, labelDict, variables, cutDict, cutArray, data)
		elif inputType == "Tree":
			# This is a bit more complicated for a tree. We have to load the actual tree structure.
			sourceName = treemakerConfig.sourceTreeName
			if not sourceName in labelDict.keys():
				print "Error: tree " + sourceName + " does not exist in the ROOT file " + ntuple + "!"
				return
			inputFile = ROOT.TFile.Open(ntuple)
			inputTree = inputFile.Get(sourceName)
			leafDict = labelDict[sourceName]
			runOverTree(inputTree, tree, runner, leafDict, variables, cutDict, cutArray, data)
			inputFile.Close()

		# Cleanup, write files to disk.
		output.cd()
		tree.Write()
		output.Write()
		output.Close()
		print "**** Finished processing file " + ntuple

	except KeyboardInterrupt:
		raise KeyboardInterruptError()

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

	# Output what input type we are.
	inputType = treemakerConfig.inputType
	if not inputType in constants.input_types:
		print "Error: invalid input format '" + inputType + "' specified!"
		sys.exit(1)
	print "*** Running treemaker in " + inputType + " mode."

	# Load the plugins once for checking before we start.
	pluginArray = plugins.loadPlugins(treemakerConfig.pluginNames, treemakerConfig.configVars, inputType=inputType)
	runner = plugins.PluginRunner(pluginArray)

	# Process "directory"; it may not, after all, be a directory now!
	ntuples, name = filelist.getNtuplesAndName(directory, name)

	# Create output name
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

	if not linear:
		pool = multiprocessing.Pool()
	results = []

	# Do splitting.
	ntuples = sorted(ntuples)
	splitNtuples, numJobs = filelist.doSplitting(ntuples, index, treemakerConfig.splitBy, treemakerConfig.splitInto)

	if len(splitNtuples) == 0:
		print "Error: no ntuples to run over!"
		return

	offset = 0
	for ntuple in splitNtuples:
#		workingNtuple = os.path.join(path, ntuple)
		workingNtuple = ntuple
		if linear:
			runOverFile(treemakerConfig, workingNtuple, outputDir, treename, offset, data)
		else:
			result = pool.apply_async(runOverFile, (treemakerConfig, workingNtuple, outputDir, treename, offset, data, ))
			results.append(result)
		offset += 1

	if not linear:
		pool.close()
		pool.join()
		for result in results:
			result.get(timeout=treemakerTimeout)

	# For now use os.system to run hadd, we should figure out a better way.
	# But this works, so...
	haddCommand = "hadd "
	if force:
		haddCommand += " -f "
	os.system(haddCommand + name + " " + outputDir + "/*")

	# Generate output cuts report.
	cuts.writeCutsReport(runner, name)

	shutil.rmtree(outputDir)
