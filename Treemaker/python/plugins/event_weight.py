import array

# Event weights, this is a pretty simple example of the 'parameters' magic.

from Treemaker.Treemaker import cuts

def setup(variables, isData):
	variables['weight'] = array.array('f', [1.0])
	return variables

def analyze(event, variables, labels, isData):
	# load the weight specified in the config file, if there is one.
	try:
		variables['weight'][0] = float(parameters['weight'])
	except:
		pass
	return variables

def reset(variables):
	variables['weight'][0] = 1.0
	return variables

def createCuts(cutArray):
	return cutArray

def makeCuts(event, variables, cutArray, labels, isData):
	return cutArray
