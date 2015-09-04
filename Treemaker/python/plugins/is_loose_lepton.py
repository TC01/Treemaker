# Check if a lepton is also 'loose'.

from Treemaker.Treemaker import cuts

numJets = 3
bMassMax = 50

def setup(variables, isData):
	return variables

def createCuts(cutArray):
	description = "Is this a loose lepton event (electron or muon)?"
	cutArray["isLoose"] = cuts.Cut("Is Loose Lepton", description)
	return cutArray

def analyze(event, variables, labels, isData):
	return variables

def makeCuts(event, variables, cutArray, labels, isData):

	muonLoose = labels['jhuMuonPFlow']['muonisloose'].product()
	electronLoose = labels['jhuElePFlow']['electronisloose'].product()
	isLoose = False

	# Check if we are a loose event.
	if variables['isElectron'][0] > 0:
		if electronLoose[0] > 0:
			isLoose = True

	elif variables['isMuon'][0] > 0:
		if muonLoose[0] > 0:
			isLoose = True

	if isLoose:
		cutArray["isLoose"].passed = 1

	return cutArray
	
def reset(variables):
	return variables
