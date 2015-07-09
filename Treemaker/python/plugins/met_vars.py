import array

# MET plugin. This is a pretty simple example.

from Treemaker.Treemaker import cuts

def setup(variables, isData):
	variables['metphi'] = array.array('f', [100.0])
	variables['metpt'] = array.array('f', [-1.0])
	return variables

def analyze(event, variables, labels, isData):
	ptHandle = labels['jhuGen']['metpt']
	phiHandle = labels['jhuGen']['metphi']
	if ptHandle.isValid() and phiHandle.isValid():
		variables['metpt'][0] = ptHandle.product()[0]
		variables['metphi'][0] = phiHandle.product()[0]
	return variables

def reset(variables):
	variables['metpt'][0] = -1.0
	variables['metphi'][0] = 100.0
	return variables

def createCuts(cutArray):
	return cutArray

def makeCuts(event, variables, cutArray, labels, isData):
	return cutArray
