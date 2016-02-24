# Z' tagjet plugin. The first part of zprime13-treemaker!

import array

from Treemaker.Treemaker import cuts

# Input type; ttree!
input_type = "Tree"

# This dictionary is filled by the config file.
parameters = {}

def setup(variables, isData):
	variables['tagJetPt'] = array.array('f', [-99.9])
	variables['tagJetEta'] = array.array('f', [-99.9])
	variables['tagJetPhi'] = array.array('f', [-99.9])
	variables['tagJetPrMass'] = array.array('f', [-99.9])
	variables['tagJetSDMass'] = array.array('f', [-99.9])
	variables['tagJetTau1'] = array.array('f', [-99.9])
	variables['tagJetTau2'] = array.array('f', [-99.9])
	variables['tagJetTau3'] = array.array('f', [-99.9])
	return variables

def analyze(event, variables, leaves, isData, cutArray):
	numAK8s = leaves['jetAK8_size']
	for i in range(min(numAK8s, 4)):		
		if leaves['jetAK8_prunedMass'][i] > 50 and leaves['jetAK8_Pt'][i] > 200 and math.fabs(leaves['jetAK8_Eta'][0]) < 2.1:
			tagJet = i
	variables['tagJetPt'][0] = leaves['jetAK8_Pt'][tagJet]
	variables['tagJetEta'][0] = leaves['jetAK8_Eta'][tagJet]
	variables['tagJetPhi'][0] = leaves['jetAK8_Phi'][tagJet]
	variables['tagJetPrMass'][0] = leaves['jetAK8_prunedMass'][tagJet]
	variables['tagJetSDMass'][0] = leaves['jetAK8_softDropMass'][tagJet]
	variables['tagJet_tau1'][0] = leaves['jetAK8_tau1'][tagJet]
	variables['tagJet_tau2'][0] = leaves['jetAK8_tau2'][tagJet]
	variables['tagJet_tau3'][0] = leaves['jetAK8_tau3'][tagJet]
	return variables, cutArray

def reset(variables):
	variables['tagJetPt'][0] = -99.9
	variables['tagJetEta'][0] = -99.9
	variables['tagJetPhi'][0] = -99.9
	variables['tagJetPrMass'][0] = -99.9
	variables['tagJetSDMass'][0] = -99.9
	variables['tagJet_tau1'][0] = -99.9
	variables['tagJet_tau2'][0] = -99.9
	variables['tagJet_tau3'][0] = -99.9
	return variables

def createCuts(cutDict):
	return cutDict

def drop(event, variables, cutArray, leaves, isData):
	#  If we tag more than one jets, we should drop the event.
	numAK8s = leaves['jetAK8_size']
	for i in range(min(numAK8s, 4)):		
		if leaves['jetAK8_prunedMass'][i] > 50 and leaves['jetAK8_Pt'][i] > 200 and math.fabs(leaves['jetAK8_Eta'][0]) < 2.1:
			nTagJets += 1
	if nTagJets != 1:
		return True
	return False