#!/usr/bin/env python

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
import labels
import plugins

# Used so trees from multiple versions do not get hadd'd together.
version = "0.1"

def runOverNtuple(ntuple, outputDir, jets, data=False):
	print "**** Processing ntuple: " + ntuple
	outputName = os.path.join(outputDir, ntuple.rpartition("/")[2])
	output = ROOT.TFile(outputName, "RECREATE")
	tree = ROOT.TTree("tree_" + version, "tree_" + version)

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
		variables = plugins.analyzePlugins(variables, labelDict, data)
		tree.Fill()
		variables = plugins.resetPlugins(variables)

	output.cd()
	tree.Write()
	output.Write()
	output.Close()
	print "**** Finished processing ntuple " + ntuple

def runTreemaker(directory, jets, data=False, force=False, name="", linear=False):
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
					runOverNtuple(workingNtuple, outputDir, jets)
				else:
					result = pool.apply_async(runOverNtuple, (workingNtuple, outputDir, jets, data, ))
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

def main():
	parser = optparse.OptionParser()
	parser.add_option("-d", "--data", dest="data", action="store_true", help="If true, we are running on data.")
	parser.add_option("-f", "--force", dest="force", action="store_true", help="If true, delete things and overwrite things.")
	parser.add_option("-l", "--linear", dest="linear", action="store_true", help="If true, disable multiprocessing.")
	parser.add_option("-j", "--jets", dest="jets", type="int", help="The number of jets to keep, defaults to 4.", default=4)
	parser.add_option("-n", "--name", dest="name", help="The name of the output file, defaults to directory name of ntuples.", default="")
	(opts, args) = parser.parse_args()

	data = opts.data
	name = opts.name
	jets = opts.jets
	force = opts.force
	linear = opts.linear
	
	# Load plugins.
	plugins.loadPlugins([], True)

	# Run the treemaker over all provided directories.
	for arg in args:
		directory = os.path.abspath(arg)
		if not os.path.exists(directory):
			print "Error: no such directory: " + arg
			sys.exit(1)
		runTreemaker(directory, jets, data, force, name, linear)

if __name__ == '__main__':
	main()
