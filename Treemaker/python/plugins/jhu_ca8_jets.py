import array
import math

import ROOT

# Variant of the jets plugin shipped by Treemaker as an example.
# Keeps the first three jhuca8 jets.
# Any per-jet variable goes in here.

# TODO: turn this back into a knob somewhere.
numJets = 3

class Jet:

	def __init__(self, number, data):
		self.number = number
		self.data = data

		self.jetName = "jet" + str(number)

		self.initVars()

	def __matchVectors(self, vectors, vector):
		"""	A modified version of MatchCol from JetTools.py, written by Marc."""
		value = -1
		deltaR = 0.4
		for i in range(len(vectors)):
			matching = ROOT.TLorentzVector()
			matching.SetPtEtaPhiM(vectors[i].Pt(), vectors[i].Eta(), vectors[i].Phi(), vectors[i].M())
			deltaR = abs(vector.DeltaR(matching))
			if deltaR < 0.4:
				value = i
		if deltaR > 0.4:
			value = -1
		return value

	def setup(self, variables):
		"""	Initializes branch arrays for all jet variables. Returns a copy of the
		variables dictionary."""
		variables[self.jetName + 'pt'] = array.array('f', [-1.0])
		variables[self.jetName + 'mass'] = array.array('f', [-1.0])
		variables[self.jetName + 'eta'] = array.array('f', [100.0])
		variables[self.jetName + 'phi'] = array.array('f', [100.0])
		variables[self.jetName + 'csv'] = array.array('f', [0.0])
		variables[self.jetName + 'tau21'] = array.array('f', [1.0])
		variables[self.jetName + 'tau32'] = array.array('f', [1.0])
		return variables

	def analyze(self, variables, labels):
		"""	Runs the treemaking step. Labels is a dictionary containing already-
		loaded handles."""
		# Do the analysis step.
		jetCollection = 'PrunedCA8'
		if not self.data:
			jetCollection += "CORR"
		jetHandle = labels['jhuCa8pp'][jetCollection]
		jetCSVHandle = labels['jhuCa8pp']['PrunedCA8csv']
		fourVector = jetHandle.product()
		csvVector = jetCSVHandle.product()
		try:
			self.mass = fourVector[self.number - 1].M()
			self.eta = fourVector[self.number - 1].Eta()
			self.phi = fourVector[self.number - 1].Phi()
			self.pt = fourVector[self.number - 1].Pt()
			self.csv = csvVector[self.number - 1]
			
			# Match the jet to the unpruned jet.
			jetVector = ROOT.TLorentzVector()
			jetVector.SetPtEtaPhiM(self.pt, self.eta, self.phi, self.mass)
			unprunedVectors = labels['jhuCa8']['UnprunedCA8'].product()
			unpruned = self.__matchVectors(unprunedVectors, jetVector)
			
			tau1 = labels['jhuCa8']['UnprunedCA8tau1'].product()
			tau2 = labels['jhuCa8']['UnprunedCA8tau1'].product()
			tau3 = labels['jhuCa8']['UnprunedCA8tau1'].product()
			if tau1[unpruned] == 0:
				self.tau21 = 100
			elif tau1[unpruned] > 0:
				self.tau21 = tau2[unpruned] / tau1[unpruned]
			if tau2[unpruned] == 0:
				self.tau32 = 100
			elif tau2[unpruned] > 0:
				self.tau32 = tau3[unpruned] / tau2[unpruned]
			
		except:
			# If this fails, set all variables to defaults.
			self.initVars()

		variables = self.update(variables)
		return variables

	def reset(self, variables):
		"""	Resets the jet variables and returns an updated copy of the variable
		array dictionary."""
		self.initVars()
		return self.update(variables)

	def update(self, variables):
		"""	Updates the actual arrays, returns an updated copy of the variable
		dictionary."""
		variables[self.jetName + 'mass'][0] = self.mass
		variables[self.jetName + 'eta'][0] = self.eta
		variables[self.jetName + 'phi'][0] = self.phi
		variables[self.jetName + 'pt'][0] = self.pt
		variables[self.jetName + 'csv'][0] = self.csv
		variables[self.jetName + 'tau21'][0] = self.tau21
		variables[self.jetName + 'tau32'][0] = self.tau32
		return variables

	def initVars(self):
		"""Initializes the jet variables to default values."""
		self.mass = -1.0
		self.pt = -1.0
		self.eta = 100
		self.phi = 100
		self.csv = 0.0
		self.tau32 = 1.0
		self.tau21 = 1.0

jets = []

def setup(variables, isData):
	global jets
	for i in xrange(numJets):
		jets.append(Jet(i + 1, isData))
		variables = jets[i].setup(variables)
	variables['numjets'] = array.array('f', [0.0])
	return variables

def createCuts(cutArray):
	return cutArray

def analyze(event, variables, labels, isData):
	# Perhaps we should write the number of jets too.
	for jet in jets:
		variables = jet.analyze(variables, labels)

	jetCollection = 'PrunedCA8'
	if not isData:
		jetCollection += "CORR"
	jetVectors = labels['jhuCa8pp'][jetCollection].product()
	variables['numjets'][0] = len(jetVectors)

	return variables

def makeCuts(event, variables, cutArray, labels, isData):
	return cutArray

def reset(variables):
	for jet in jets:
		variables = jet.reset(variables)
	variables['numjets'][0] = 0.0
	return variables
