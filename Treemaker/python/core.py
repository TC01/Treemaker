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
		
	# Now, run over all events.
	for event in Events(ntuple):
		labelDict = labels.fillLabels(event, labelDict)
		variables = plugins.analyzePlugins(event, variables, labelDict, data)
		tree.Fill()
		variables = plugins.resetPlugins(variables)

	output.cd()
	tree.Write()
	output.Write()
	output.Close()
	print "**** Finished processing ntuple " + ntuple

def runTreemaker(directory, treename="tree", data=False, force=False, name="", linear=False):
	print "*** Running treemaker over " + directory
	if name == "":
		name = directory.rpartition("/")[2]
	if not ".root" in name:
		name += ".root"
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

	for path, dirs, files in os.walk(directory):
		if path == directory:
			for ntuple in files:
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

	shutil.rmtree(outputDir)
