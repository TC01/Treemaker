#!/usr/bin/env python

import array
import multiprocessing
import optparse
import os
import shutil
import sys

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from DataFormats.FWLite import Events, Handle

# Used so trees from multiple versions do not get hadd'd together.
version = "0.1_alpha"

correction = "CORR"
label = ("diffmoca8pp", "PrunedCA8" + correction)
handle = Handle("vector<ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> > > ")

class Jet:

	def __init__(self, number):
		self.number = number

		# Properties we are interested in.
		self.reset()

	def constructArray(self):
		booked = {}
		booked['pt'] = array.array('f', [-1.0])
		booked['mass'] = array.array('f', [-1.0])
		booked['eta'] = array.array('f', [100.0])
		booked['phi'] = array.array('f', [100.0])
		return booked

	def fillArray(self, event, booked):
		event.getByLabel(label, handle)
		fourVector = handle.product()
		try:
			self.mass = fourVector[self.number - 1].M()
			self.eta = fourVector[self.number - 1].Eta()
			self.phi = fourVector[self.number - 1].Phi()
			self.pt = fourVector[self.number - 1].Pt()
		except:
			self.reset()

		# Update the booking 'array'.
		booked['pt'][0] = self.pt
		booked['mass'][0] = self.mass
		booked['eta'][0] = self.eta
		booked['phi'][0] = self.phi
		return booked

	def reset(self):
		self.mass = -1.0
		self.pt = -1.0
		self.eta = 100
		self.phi = 100
		self.csv = 0.0
		self.tau32 = 1.0
		self.tau21 = 1.0

def runOverNtuple(ntuple, outputDir, jets):
	print "**** Processing ntuple: " + ntuple
	outputName = os.path.join(outputDir, ntuple.rpartition("/")[2])
	output = ROOT.TFile(outputName, "RECREATE")
	tree = ROOT.TTree("tree_" + version, "tree_" + version)

	bookArray = []
	jetArray = []
	for i in xrange(jets):
		jet = Jet(i + 1)
		jetArray.append(jet)
		booked = jet.constructArray()
		bookArray.append(booked)
		
		for key in booked.iterkeys():
			name = "jet" + str(i+1) + key
			tree.Branch(name, booked[key], name + '/F') 

	for event in Events(ntuple):		
		for i in xrange(jets):
			bookArray[i] = jetArray[i].fillArray(event, bookArray[i])
		tree.Fill()
		for jet in jetArray:
			jet.reset()

	output.cd()
	tree.Write()
	output.Write()
	output.Close()
	print "**** Finished processing ntuple."

def runTreemaker(directory, jets, force=False, name="", linear=False):
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
					result = pool.apply_async(runOverNtuple, (workingNtuple, outputDir, jets,))
					results.append(result)

	pool.close()
	pool.join()

	# For now use os.system:
	haddCommand = "hadd "
	if force:
		haddCommand += " -f "
	os.system(haddCommand + name + " " + outputDir + "/*")

	shutil.rmtree(outputDir)

def main():
	parser = optparse.OptionParser()
	parser.add_option("-f", "--force", dest="force", action="store_true", help="If true, delete things and overwrite things.")
	parser.add_option("-l", "--linear", dest="linear", action="store_true", help="If true, disable multiprocessing.")
	parser.add_option("-j", "--jets", dest="jets", type="int", help="The number of jets to keep, defaults to 4.", default=4)
	parser.add_option("-n", "--name", dest="name", help="The name of the output file, defaults to directory name of ntuples.", default="")
	(opts, args) = parser.parse_args()

	name = opts.name
	jets = opts.jets
	force = opts.force
	linear = opts.linear

	for arg in args:
		directory = os.path.abspath(arg)
		if not os.path.exists(directory):
			print "Error: no such directory: " + arg
			sys.exit(1)
		runTreemaker(directory, jets, force, name, linear)

if __name__ == '__main__':
	main()
