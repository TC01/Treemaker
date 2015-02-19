# An example cut that I used in the old G* analysis.

from Treemaker.Treemaker import cuts

def setup(variables, isData):
	return variables

def createCuts(cutArray):
	description = "An example cut that was used as a preselection in the G* hadronic analysis."
	cutArray["gstar_preselection"] = cuts.Cut("G* preselection", description)
	return cutArray
	
def analyze(event, variables, labels, isData):
	return variables
	
def makeCuts(event, variables, cutArray, labels, isData):
	jetCollection = 'PrunedCA8'
	if not self.data:
		jetCollection += "CORR"
	jetHandle = labels['diffmoca8pp']['PrunedCA8']
	fourVector = jetHandle.product()
	try:
		if fourVector[3].M() > 50:
			cutArray["gstar_preselection"].passed = 1
		else:
			raise RuntimeError
	except:
		cutArray["gstar_preselection"].passed = 0
	
	return cutArray
	
def reset(variables):
	return variables
