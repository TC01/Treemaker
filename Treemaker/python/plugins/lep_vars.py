import array

# Leptons plugin. This plugin also has some cuts for is_muon and is_electron.
# (and is_had, of course).

from Treemaker.Treemaker import cuts

etaCutoff = 2.4
ptCutoff = 10

def setup(variables, isData):
	variables['lepphi'] = array.array('f', [100.0])
	variables['leppt'] = array.array('f', [-1.0])
	variables['lepeta'] = array.array('f', [100.0])
	variables['lepmass'] = array.array('f', [-1.0])

	variables['lepcharge'] = array.array('f', [0.0])
	variables['lepiso'] = array.array('f', [-1.0])

	variables['isMuon'] = array.array('f', [0.0])
	variables['isElectron'] = array.array('f', [0.0])

	return variables

def fillLeptons(variables, vector, iso, charge):
	variables['leppt'][0] = vector[0].Pt()
	variables['lepphi'][0] = vector[0].Phi()
	variables['lepeta'][0] = vector[0].Eta()
	variables['lepmass'][0] = vector[0].M()
	variables['lepcharge'][0] = charge[0]
	variables['lepiso'][0] = iso[0]
	return variables

def analyze(event, variables, labels, isData, cutArray):
	electrons = labels['jhuElePFlow']['electron'].product()
	muons = labels['jhuMuonPFlow']['muon'].product()
	
	electronCharge = labels['jhuElePFlow']['electroncharge'].product()
	muonCharge = labels['jhuMuonPFlow']['muoncharge'].product()

	electronISO = labels['jhuElePFlow']['electroniso'].product()
	muonISO = labels['jhuMuonPFlow']['muoniso'].product()

	# Do nothing if there are no electrons *or* muons.
	if len(electrons) == 0 and len(muons) == 0:
		return variables, cutArray
	
	# Sort into three different categories: only the muons and electrons one
	# is hard.
	if len(electrons) == 0 and len(muons) > 0:
		if muons[0].Eta() < etaCutoff and muons[0].Pt() > ptCutoff:
			variables = fillLeptons(variables, muons, muonISO, muonCharge)
			variables['isMuon'][0] = 1.0
	elif len(electrons) > 0 and len(muons) == 0:
		if electrons[0].Eta() < etaCutoff and electrons[0].Pt() > ptCutoff:
			variables = fillLeptons(variables, electrons, electronISO, electronCharge)
			variables['isElectron'][0] = 1.0
	else:
		if electrons[0].Eta() < etaCutoff and electrons[0].Pt() > muons[0].Pt() and electrons[0].Pt() > ptCutoff:
			variables = fillLeptons(variables, electrons, electronISO, electronCharge)
			variables['isElectron'][0] = 1.0
		if muons[0].Eta() < etaCutoff and muons[0].Pt() > electrons[0].Pt() and muons[0].Pt() > ptCutoff:
			variables = fillLeptons(variables, muons, muonISO, muonCharge)
			variables['isMuon'][0] = 1.0
		
	# For legacy purposes.
	if variables['isElectron'][0] > 0:
		cutArray['isElectron'].passed = 1
	if variables['isMuon'][0] > 0:
		cutArray['isMuon'].passed = 1


	return variables, cutArray

def reset(variables):
	variables['leppt'][0] = -1.0
	variables['lepphi'][0] = 100.0
	variables['lepeta'][0] = 100.0
	variables['lepmass'][0] = -1.0

	variables['lepcharge'][0] = 0.0
	variables['lepiso'][0] = -1.0

	variables['isMuon'][0] = 0.0
	variables['isElectron'][0] = 0.0

	return variables

def createCuts(cutArray):
	cutArray["isHadronic"] = cuts.Cut("Hadronic", "Is the event purely hadronic?")
	cutArray["isMuon"] = cuts.Cut("Muon", "Is the event a muon event?")
	cutArray["isElectron"] = cuts.Cut("Electron", "Is the event an electron event?")
	return cutArray

def drop(event, variables, cutArray, labels, isData):
	# Drop non-leptonic events.
	if cutArray['isElectron'].passed == 0 and cutArray['isMuon'].passed == 0:
		return True
	return False
